
from main import get_news
import pickle
from time import time

ai_tags = ["生成","AI","業務用"]
# now = datetime.now().strftime("%Y-%m-%d-%H")
with open(f'../cache/result.inn', 'wb') as file: #TODO エラー処理必要か
    print("main.py実行中 ...")
    start = time()
    news = get_news(ai_tags)
    end = time()
    pickle.dump(news,file)
    print("完了")
    print(f"実行時間 get_news(): {end - start} s")
    print()
    print(f"出力ファイル : result.inn")
