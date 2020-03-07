import re
import requests

url = 'https://pvp.qq.com/web201605/herodetail/%s.shtml'
img_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{0}/{0}-bigskin-{1}.jpg'

for hero in requests.get('https://pvp.qq.com/web201605/js/herolist.json').json():
    result = requests.get(url % hero['ename'])
    result.encoding = 'gbk'
    t = re.findall('data-imgname="(.*?)"', result.text)
    # 苍天翔龙&0|忍●炎影&1|未来纪元&1|皇家上将&6|嘻哈天王&1|白执事&1|引擎之心&5"
    skin_num = re.sub('&\d+', '', t[0]).split('|')
    # 抓取图片到本地
    for index, skin_name in enumerate(skin_num, 1):
        img_result = requests.get(img_url.format(hero['ename'], index))
        file_path = f"{hero['ename']}_{hero['cname']}_{index}_{skin_name}.jpg"
        with open(file_path, 'wb') as f:
            f.write(img_result.content)
        print("下载皮肤", index, file_path)
# 共计 391 个皮肤
