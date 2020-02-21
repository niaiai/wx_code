import time
import pymysql
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

start_time = time.time()  # 计算程序运行时间
url = 'http://s.askci.com/stock/a/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

mysql_host = 'localhost'
mysql_password = '******'
mysql_db = 'python_spider'
rename = {
    "上市日期": "listing_date",
    "主营业务": "main_business",
    "主营业务收入(201909)": "main_bussiness_income",
    "产品类型": "industry_type",
    "公司名称": "company_name",
    "公司财报": "financial_report",
    "净利润(201909)": "net_profit",
    "员工人数": "employees",
    "城市": "city",
    "序号": "serial_number",
    "招股书": "prospectuses",
    "省份": "province",
    "股票代码": "stock_code",
    "股票简称": "stock_abbre",
    "行业分类": "industry_classification"
}
create_table_sql = """CREATE TABLE IF NOT EXISTS listed_company (
    serial_number INT(20) NOT NULL,
    stock_code INT(20) ,
    stock_abbre VARCHAR(20) ,
    company_name VARCHAR(100) ,
    province VARCHAR(20) ,
    city VARCHAR(20) ,
    main_bussiness_income VARCHAR(20) ,
    net_profit VARCHAR(20) ,
    employees VARCHAR(20) ,
    listing_date DATETIME(0) ,
    prospectuses VARCHAR(20) ,
    financial_report VARCHAR(20) ,
    industry_classification VARCHAR(100) ,
    industry_type VARCHAR(400) ,
    main_business VARCHAR(400) ,
PRIMARY KEY (serial_number)
)"""


def generate_mysql():
    print("生成数据表字段")
    conn = pymysql.connect(
        host=mysql_host,
        user='root',
        password=mysql_password,
        port=3306,
        charset='utf8',
        db=mysql_db)
    cursor = conn.cursor()

    cursor.execute(create_table_sql)
    conn.close()


# 第一步: 下载网页
def get_one_page(page):
    try:
        paras = {
            'reportTime': '2019-09-30',  # 可以改报告日期，比如2018-6-30获得的就是该季度的信息
            'pageNum': page  # 页码
        }
        response = requests.get(url, params=paras, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        print('爬取失败')


# 第二步: 从网页中解析所需内容
def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select('#myTable04')[0]  # [0]将返回的list改为bs4类型
    tbl = pd.read_html(content.prettify(), header=0)[0]
    # prettify()优化代码,[0]从pd.read_html返回的list中提取出DataFrame
    tbl.rename(columns=rename, inplace=True)
    return tbl


# 第三步: 导入到数据库
def write_to_sql(tbl, engine):
    try:
        tbl.to_sql('listed_company', con=engine, if_exists='append', index=False)
        # append表示在原有表基础上增加，但该表要有表头
    except Exception as e:
        print(e)


def spider_one_page(page):
    print("抓取第{}页".format(page))
    html = get_one_page(page)
    tbl = parse_one_page(html)
    write_to_sql(tbl, db_engine)


# 需要抓取的总页数
pages = 186
# 数据库引擎
db_engine = create_engine('mysql+pymysql://root:{}@{}:3306/{}?charset=utf8'.format(mysql_password, mysql_host, mysql_db))


# if __name__ == '__main__':
#     print("单进程爬取")
#     generate_mysql()
#
#     for i in range(1, pages):
#         spider_one_page(i)
#     endtime = time.time() - start_time
#     print('程序运行了%.2f秒' % endtime)


from multiprocessing import Pool

if __name__ == '__main__':
    # 数据库引擎
    generate_mysql()
    pool = Pool(4)
    print("多进程爬取")
    pool.map(spider_one_page, range(1, pages))
    endtime = time.time() - start_time
    pool.close()
    print('程序运行了%.2f秒' % (time.time() - start_time))
