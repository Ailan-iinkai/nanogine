import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key =  os.getenv('OPEN_API_KEY')

def func(picup_data):
    # 取得した記事ごとに要約を行う
    for article_id, article_info in picup_data.items():
        # 要約するテキスト
        text_to_summarize = article_info.context

        # OpenAIへリクエストを送信
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "あなたは新聞記者です"},
            {"role": "assistant", "content": text_to_summarize},
            {"role": "user", "content": "この記事をそれぞれ300字程度に要約してください"},
          ],
          max_tokens=500,  # outputトークン数の上限
          stop=["\n"]
        )

        # 要約されたテキストを取得
        summary = response['choices'][0]['message']['content']

        # 要約を出力
        print(f"記事ID: {article_id}")
        print(f"記事タイトル: {article_info.title}")
        print("要約:")
        print(summary)
        print("\n" + "-" * 50 + "\n")