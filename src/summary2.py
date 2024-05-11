import os
import pickle
import openai
from collections import namedtuple
import tiktoken
import sys
from error import log
from dotenv import load_dotenv
load_dotenv()

openai.api_key =  os.getenv('OPEN_API_KEY')
enc=tiktoken.get_encoding("gpt2")

# namedtupleを定義
ArticleSummary = namedtuple('ArticleSummary', ['title', 'url', 'summary'])

# 取得した記事ごとに要約を行う
def summarize_articles(picup_data):

    summaries = {}

    for article_id, article_info in picup_data.items():
        text_to_summarize = article_info.context
        title = article_info.title
        url = article_info.url

        messages=[
                {"role": "system", "content": "あなたは新聞記者です"},
                {"role": "assistant", "content": text_to_summarize},
                {"role": "user", "content": "この記事をそれぞれ300字程度に要約してください"},
            ]
        
        #token検証
        tokens = enc.encode("\n".join([f"{msg['role']}:{msg['content']}" for msg in messages])) #messagesをgpt2モデルでトークン化
        tolerance = 3500
        if len(tokens) > tolerance:
            err_msg = f"token数が{tolerance}を超えているため、処理をスキップしました."
            err_detail = {"token_count": len(tokens), "title": title, "len(text_to_summarize)": len(text_to_summarize), "url": url}
            log(err_msg, err_detail)
            continue #token数が3500以上の場合エラー処理を飛ばす

        #OpenAIへリクエストを送信
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,# urlとtitleの取得を確認するために一時的に最大トークン数を減少
            stop=["\n"]
        )

        # 要約された記事を取得
        summary = response['choices'][0]['message']['content']
        # namedtupleを使用してsummariesに追加
        summaries[article_id] = ArticleSummary(title=title, url=url, summary=summary)

    return summaries
