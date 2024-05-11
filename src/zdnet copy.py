import requests
from bs4 import BeautifulSoup

# arc_ttl,arc_lnklist,arc_contをネームドタプルに
from collections import namedtuple

def zdnet():
  arc_lnklist = []
  arc_ttl = []
  arc_cont = []

  url = "https://japan.zdnet.com/"
  r = requests.get(url)
  soup = BeautifulSoup(r.content, "html.parser")

  # リンク取得（リスト型：arc_lnklist）
  target = soup.find_all('a', {'data-ga_category': 'zd_top_list_new'})
  arc_lnk_tag = [x["href"] for x in target]

  # for分でリンクをリスト化
  for x in arc_lnk_tag:
    modified_lnk = "https://japan.zdnet.com" + x
    arc_lnklist.append(modified_lnk)

  # 取得したリンクで記事一覧→記事ページへ飛んでtitle,contを取得
  # title（リンク型：arc_ttl）、cont（リンク型：arc_cont）
  for x in range(len(arc_lnklist)):
      cont_list = [0] * 10
      arcurl = arc_lnklist[x]
      arcr = requests.get(arcurl)
      arcsoup = BeautifulSoup(arcr.content, "html.parser")
      # title取得
      ttl = arcsoup.find('h1', id="story_title_disp")
      arc_ttl.append(ttl.text)
      # cont取得
      # 1ページ目
      cont_tags = arcsoup.find('div', class_="article-contents").find_all("p")
      cont_fortext = [tag.text.strip() for tag in cont_tags]

      for y in range(len(cont_fortext)):
          cont_join = "".join(cont_fortext)

      cont_list[0] = cont_join
      
      # 2ページ目以降が存在する場合には、取得
      for page_number in range(2, 10):
        arcurl_extra = f"{arcurl}/{page_number}/"
        arcr_extra = requests.get(arcurl_extra)
        if arcr_extra.status_code == 200:
          arcsoup_extra = BeautifulSoup(arcr_extra.content, "html.parser")
          cont_tags = arcsoup_extra.find('div', class_="article-contents").find_all("p")
          cont_fortext = [tag.text.strip() for tag in cont_tags]
          # ページの全文結合
          for y in range(len(cont_fortext)):
            cont_join = "".join(cont_fortext)
          # コントリストへ格納
          cont_list[page_number-1] = cont_join

      # 無駄な要素の削除
      cont_list = [x for x in cont_list if x != 0]

      # 記事全文の結合
      for y in range(len(cont_list)):
        cont_merge = "".join(cont_list)
      
      # 全ページからcontを取得したら、リスト格納  
      arc_cont.append(cont_merge)

  # arc_ttl,arc_lnklist,arc_contをネームドタプルに
  # namedtupleの定義
  Article = namedtuple('zdarticle', ['title', 'context', 'url'])

  # 辞書にデータをまとめる
  data = {i: Article(t, c, u) for i, (t, c, u) in enumerate(zip(arc_ttl, arc_cont, arc_lnklist), start=1)}

  return data