from urllib.parse import urljoin
import pandas as pd
from tqdm import tqdm
from urllib import request
from bs4 import BeautifulSoup

# stock_URL.csvの読み込み
url_list = pd.read_csv("page_URL.csv", index_col=0)
url_df = pd.DataFrame(url_list)
pages = {}
Table = pd.DataFrame()


# ページを選択してそのページ内の企業urlを取得する
def Stock_Data_Get():
    for page in tqdm(list(url_df.iloc[:, 0]), desc='first'):
        u_page = page.split('=')[1]

        # pageを辞書に格納
        pages[u_page] = [page]

    page_num = input("ページ数を入力:")
    page_s = pages[page_num]

    # 入力したページのhtmlを取得
    base_page = "".join(page_s)
    html = request.urlopen(base_page)
    soup = BeautifulSoup(html, "html.parser")
    url = []

    for t in tqdm(soup.find_all("a"), desc='second'):
        url.append(''.join(list(urljoin(base_page, t.get('href')))))

    Table = pd.DataFrame(url)
    # display(Table)

    # 入力したページの企業urlテーブルを取得
    Table = Table.iloc[range(8, 128), 0]

    Table.reset_index(inplace=True, drop=True)
    Table.to_csv('page_' + page_num + '.csv', header=True)

    # データの欲しい企業番号を入力してurlを取得
    global C_num
    C_num = input("stock_num:")
    global st_url
    st_url = "https://kabuoji3.com/stock/" + C_num + "/"
    print(st_url)


def Data_Soup():
    tables = pd.read_html(st_url, flavor='bs4', index_col=0)
    df_1 = pd.DataFrame(tables[0])
    global dfs_2

    # -- tables[0]と[1]を結合 ---

    if tables[1] is not None:
        df_2 = pd.DataFrame(tables[1])
        dfs_2 = pd.concat([df_1, df_2])
        dfs_2 = dfs_2.reset_index()
    else:
        dfs_2 = df_1.reset_index()

    # --------------------------

    # dfs_2 = df_1.reset_index()
    print("dfs_2を出力\n", dfs_2)

    x = dfs_2['日付'][-1::-1].reset_index(drop=True)
    y = dfs_2['終値'][-1::-1].reset_index(drop=True)


if __name__ == '__main__':
    Stock_Data_Get()
    Data_Soup()
