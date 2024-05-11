import os
import random
import sqlite3
import sys
import threading
import os
current_file_path = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file_path)
sys.path.append(current_directory)
sys.path.append(os.path.join(current_directory,"src"))
from datetime import datetime
import pickle
from flask import Flask, jsonify, make_response, redirect, url_for, request
from flask import render_template
from src.main import get_news
from src.result_filter import tags as loadtag
from util.generater import generate_html_from_yaml, valid_cache
from pprint import pprint


if os.path.exists('.env'):
    pass
else:
    api_key = input("openAIのAPIキー:")
    with open(".env", "w") as f:
        f.write(f"OPEN_API_KEY={api_key}")
app = Flask(__name__)


dbfile = 'nanogine.db'



loaded_data = {}
now = datetime.now().strftime("%Y-%m-%d-%H")
if os.path.exists("cache/result.inn"): 
    try:
        with open(f'cache/result.inn', 'rb') as file:
            loaded_data = pickle.load(file)
    except:
        pass



@app.route('/article') #DB取得の例
def article():
    db = sqlite3.connect(dbfile) #db接続
    db.row_factory = sqlite3.Row #カラム名でアクセスできるように
    cursor = db.cursor()
    query = "SELECT * FROM article"

    cursor.execute(query)
    articles = cursor.fetchall()
    title_list = []
    for article in articles:
        title = article['title']
        title_list.append(title)
    return render_template('article.html', article_titles=title_list)

@app.route('/') #tune magagineテンプレートへの適応
def tune():
    if os.path.exists('nanogine.db'):
        pass
    else:
        return redirect(url_for('picup'))
    db = sqlite3.connect(dbfile) #db接続
    db.row_factory = sqlite3.Row #カラム名でアクセスできるように
    cursor = db.cursor()
    query = "SELECT group_id FROM article ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    group_id = cursor.fetchone()['group_id']
    query = f"SELECT * FROM article where group_id = {group_id}"
    cursor.execute(query)
    articles = cursor.fetchall()
    article_list = []
    for article in articles:
        article_list.append(
            {'title': article['title'],
            'context': article['context'],
            'date': article['date'],
            'url': article['url']}
            )
    return render_template('TUNE magazine.html',data=article_list)


@app.route('/picup') #ホーム(試験的)
def picup(): 
    if os.path.exists("cache/tags.inn"):
        thread = threading.Thread(target=update)
        print("call .update()")
        thread.start()
        htmls = ['loading_cat.html','loading.html']
        choiced_html = random.choices(htmls, weights=[1, 2], k=1)[0]
        return render_template(choiced_html)
    else:
        return redirect(url_for('tags_select'))

@app.route('/picup/result')
def picup_result(): 
    if os.path.exists("cache/main_result.inn"):
        pass
    else:
        message = {"status":"loading","msg": ""}
        with open('cache/main_result.inn','wb') as f:
            pickle.dump(message,f)
    with open('cache/main_result.inn','rb') as f:
        result = pickle.load(f)
        match result['status']:
            case "ok":
                message = {"status":"none","msg": ""}
                with open('cache/main_result.inn','wb') as f:
                    pickle.dump(message,f)
                response_content = {"message": "finish"}
                response = make_response(jsonify(response_content))
                response.status_code = 200
                return response
            case "failed":
                message = {"status":"none","msg": ""}
                with open('cache/main_result.inn','wb') as f:
                    pickle.dump(message,f)
                error_message = result['msg']
                response_content = {"message": f"{error_message}"}
                response = make_response(jsonify(response_content))
                response.status_code = 500
                return response
            case "loading":
                response_content = {"message": "loading"}
                response = make_response(jsonify(response_content))
                response.status_code = 204
                return response

def update(): #ニュース取得
    if os.path.exists("cache/tags.inn"):
        tags = None
        with open(f'cache/tags.inn', 'rb') as file:
            tags = pickle.load(file)
        print(f'[info] Tags: {tags}')
        print('[info] Start main.get_news')
        news =get_news(tags)
        print('[info] End main.get_news')
        with open(f'cache/result.inn', 'wb') as file:
            pickle.dump(news,file)
    else:
        print('[info] Skip main.get_news. File not found cache/tags.inn')    

@app.route('/tags/select') #タグ選択
def tags_select():
    tags = loadtag()
    html = generate_html_from_yaml(tags)
    return html

@app.route('/receive_tags', methods=['POST'])
def receive_tags():
    data = request.json
    print(f"[Info] Received Data: {data}")

    with open(f'cache/tags.inn', 'wb') as file:
        pickle.dump(data,file)
    return 'Data received successfully'

@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)

