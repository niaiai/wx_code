import pandas as pd
for page in range(1, 4):  # 爬取全部页
    df = pd.read_html('http://s.askci.com/stock/a/?reportTime=2019-09-30&pageNum=%s' % page)[3]
    df.to_csv('A股公司信息_5LineCode.csv', mode='a', encoding='utf_8_sig', index=False)
