import os
import json
import pickle
import sqlite3
from datetime import datetime
import traceback
from zdnet import zdnet
from result_filter import search, check_duplication
from summary2 import summarize_articles
from time import time
from error import log

def get_news(tags):
    try:
        message = {"status":"loading","msg": ""}
        with open('cache/main_result.inn','wb') as f:
            pickle.dump(message,f)
        # 谷崎
        print("ニュース取得中 ...")
        start = time()
        data = zdnet()
        end = time()
        print("ニュース取得完了!")
        print(f"実行時間 zdnet(): {end - start} s")
        print()
        if len(data) == 0:
            return {}
        # 織茂
        print("フィルタリング中 ...")
        start = time()
        data = search(data,tags)
        end = time()
        print("フィルタリング完了!")
        print(f"実行時間 search(): {end - start} s")
        print()
        if len(data) == 0:
            return {}

        # 周りたち
        print("要約中 ...")
        start = time()
        news = summarize_articles(data)
        end = time()
        print("要約完了!")
        print(f"実行時間 summarize_articles(): {end - start} s")
        print()
        if len(data) == 0:
            return {}
        print("DB保存中 ...")
        start = time()
        save_db(news,tags)
        end = time()
        print("DB保存完了!")
        print(f"実行時間 save_db(): {end - start} s")
        print()
        message = {"status":"ok","msg": ""}
        with open('cache/main_result.inn','wb') as f:
            pickle.dump(message,f)
        return news
    except Exception as e:
        stack_trace = traceback.format_exc()
        error_message = {"status":"failed","msg": str(e)} #status ok , failed, none
        with open("cache/main_result.inn", "wb") as f:
            pickle.dump(error_message, f)
        err_msg = f"問題が発生しました"
        err_detail = {"error": e,"stack_trace":stack_trace}
        log(err_msg, err_detail)

def save_db(data: dict,tags):
    """"""
    date = datetime.now()
    group_id = str(int(date.timestamp()))
    
    if os.path.exists('nanogine.db'):
        conn = sqlite3.connect(f'nanogine.db',timeout=10)
    else:
        try:
            conn = sqlite3.connect(f'nanogine.db',timeout=10)
            conn.execute("""CREATE TABLE article (
            id TEXT PRIMARY KEY,
            group_id INTEGER,
            article_id INTEGER UNIQUE,
            title TEXT,
            context TEXT,
            url TEXT,
            pic_id TEXT,
            tag_set_id TEXT,
            date DATETIME,
            FOREIGN KEY (tag_set_id) REFERENCES tag_set(id),
            FOREIGN KEY (pic_id) REFERENCES thumbnail(id)
            );""")

            conn.execute("""CREATE TABLE tag_set (
                id TEXT PRIMARY KEY,
                name TEXT,
                tags TEXT,
                date DATETIME
            );""")

            conn.execute("""CREATE TABLE thumbnail (
                id TEXT PRIMARY KEY,
                pic BLOB,
                date DATETIME
            );""")
        except sqlite3.DatabaseError as e:
            raise e
        except IOError as e:
            raise e
    if data:
        pass
    else:
        return
    for i, article in data.items():
        article_id = group_id + f"{i:05d}"
        title = article.title
        context = article.summary
        url = article.url
        pic_id = None
        tag_set_id = group_id
        conn.execute("INSERT INTO article (group_id, article_id, title, context, url, pic_id, tag_set_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (group_id, article_id, title, context, url, pic_id, tag_set_id, date))

    name = f"{datetime.now()}"
    json_tags = json.dumps({"flat": tags},ensure_ascii=False)
    conn.execute("INSERT INTO tag_set (id, name, tags, date) VALUES (?, ?, ?, ?)",(group_id, name, json_tags, date))

        # pic = 'sample'.encode('utf-8') 
        # conn.execute(
        #     "INSERT INTO thumbnail (id, pic, date) VALUES (?, ?, ?)",
        #     (pic_id, pic, date)
        # )

    conn.commit()
    conn.close()
