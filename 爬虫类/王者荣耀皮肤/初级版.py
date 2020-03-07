import requests

img_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{0}/{0}-bigskin-{1}.jpg'
for hero in requests.get('https://pvp.qq.com/web201605/js/herolist.json').json():
    skin_names = hero.get('skin_name', '').split('|')
    for index, skin_name in enumerate(skin_names, 1):
        file_path = f"{hero['ename']}_{hero['cname']}_{index}_{skin_name}.jpg"
        img_result = requests.get(img_url.format(hero['ename'], index))
        with open(file_path, 'wb') as f:
            f.write(img_result.content)
# 共计 341 个皮肤
