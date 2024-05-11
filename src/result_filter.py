
import os
from pathlib import Path
import pickle
import sqlite3
from typing import List
from janome.tokenizer import Tokenizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import yaml

setting_dir = Path(__file__).parent/'setting'

def tokenize(text):
    """Janomeを使用してテキストをトークン化"""
    tokenizer = Tokenizer()
    tokens = [token.surface for token in tokenizer.tokenize(text)]
    return tokens

def vectorizer():
    file = setting_dir/'stop_word.txt'
    with open(file,'r') as f:
        stopwords = [line.strip() for line in f.readlines()]
    vectorizer = TfidfVectorizer(stop_words=stopwords,ngram_range=(1,2)) #TODO 微調整必要か
    return vectorizer

def vectorize(tokens:list,vectorizer:TfidfVectorizer):
    vector = vectorizer.fit_transform(tokens)
    return vector

def vectorize_tags(taglist:list[str],vectorizer:TfidfVectorizer):
    return vectorizer.transform(taglist)
    
def sparse(text_vec,tags_vec):
    n_dims = text_vec.shape[1]
    if tags_vec.shape[1] < n_dims:
        filler = np.zeros((tags_vec.shape[0], n_dims - tags_vec.shape[1]))
        tags_vec = np.hstack((tags_vec, filler))
    return tags_vec

def relative_score_cos(text: str, taglist: list[str]):
    """textのトークンとtaglistのコサイン類似度で比較"""
    vec = vectorizer()
    text_vec = vectorize(tokenize(text),vec)
    tags_vec = vectorize_tags(taglist,vec)
    tags_vec = sparse(text_vec,tags_vec)
    similarity = cosine_similarity(text_vec, tags_vec)
    mask = np.eye(similarity.shape[0], similarity.shape[1], dtype=bool)
    scores = similarity[~mask].mean()
    return scores


def relative_score_count(text: str, user_input: list[str]):
    text_tokens = tokenize(text)
    user_tokens = set(user_input) 

    # ユーザーの関心単語とテキスト内の単語の登場回数を計算
    match_count = sum(1 for word in user_tokens if word in text_tokens)
    max_score = len(user_tokens)  # ユーザーの関心単語の総数
    relative_score = match_count / max_score if max_score > 0 else 0

    return relative_score

def search(data:dict, search_strings:List[str]) -> dict:
        """部分一致検索

        Args:
            data (dict): スクレイピングデータ
            search_strings (list): フィルタタグ

        Returns:
            filterd_data (dict): search_stringsのいずれかの要素に一致する要素
        """

        data = check_duplication(data)
        if len(data) == 0:
            return data
        data_score = dict.fromkeys(data.keys(), 0)

        for i, value in data.items():
            title_score = relative_score_cos(value.title, search_strings)
            context_score = relative_score_cos(value.context, search_strings)
            score = title_score * 2 + context_score #タイトルスコアを2倍に
            data_score[i] = score
        data_score = sorted(data_score.items(), key=lambda x: x[1], reverse=True)
        data_score = data_score[:6]
        print(data_score) #XXX debug用
        picup_data = {}
        for i in data_score:
            picup_data[i[0]] = data[i[0]]

        return  picup_data


def check_duplication(data:dict):
    newer_data = {}
    if os.path.exists('nanogine.db'):
        conn = sqlite3.connect(f'nanogine.db',timeout=10)
        c = conn.cursor()
        c.execute("SELECT MAX(group_id) FROM article;")
        latest_group = c.fetchone()[0]
        c.execute("SELECT title FROM article WHERE group_id = ?;", (latest_group,))
        latest_titles = set(row[0] for row in c.fetchall())
        for i, article in data.items():
            if article.title in latest_titles:
                pass
            else:
                newer_data[i] = data[i]
    else:
        newer_data = data
    return newer_data


def tags():
    file = setting_dir/'tags.yml'
    with open(file, "r") as f:
        tags = yaml.load(f, Loader=yaml.FullLoader)
        tags = tags['tags']
    return tags
        
