import requests
from lxml import etree
import time
from random import randint

def anime_crawler():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

    print("L9: request start")

    response = requests.get("https://ani.gamer.com.tw/", headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        content = response.content.decode()
        html = etree.HTML(content)
        print(html)
        return "網站請求失敗"


    print("L16: request finish")

    titles = html.xpath(f"//*[@class='animate-theme-list']/div[@class='theme-title-block']/h1/text()")
    title_index = [i-1 for i, item in enumerate(titles) if "授權到期節目" in item]

    if len(title_index) != 0:
        print(title_index)

        anime_name = []
        anime_episode = []
        anime_year = []
        anime_urls = []
        removal_date  = []

        for index in title_index:
            names = html.xpath(f"//*[@id='blockAnimeNewArrive-{str(index)}']/div[2]/a/div[2]/div[2]/p/text()")
            anime_name.extend([name.strip() for name in names])

            episodes = html.xpath(f"//*[@id='blockAnimeNewArrive-{str(index)}']/div[2]/a/div[2]/div[2]/div/span/text()")
            anime_episode.extend([episode.strip() for episode in episodes])

            year = html.xpath(f"//*[@id='blockAnimeNewArrive-{str(index)}']/div[2]/a/div[2]/div[2]/div/p/text()")
            anime_year.extend([y.strip()[3:] for y in year])

            urls = html.xpath(f"//*[@id='blockAnimeNewArrive-{str(index)}']/div[2]/a/@href")
            anime_urls.extend(["https://ani.gamer.com.tw/" + url for url in urls])

        for url in anime_urls:
            anime_response = requests.get(url, headers=headers)
            print(url, anime_response.status_code)
            anime_content = anime_response.content.decode()
            anime_html = etree.HTML(anime_content)

            removal_date.append("".join(d[7:] for d in anime_html.xpath("//div[2]/div[1]/section/div[2]/div/p[2]/text()")))

            time.sleep(randint(5, 10))


        return list(zip(anime_name, anime_episode, anime_year, anime_urls, removal_date))

    else:
        return "無授權即將到期動畫"


print(anime_crawler())


'''
for index in title_index:
    # 抓取整個區塊的資料
    block = html.xpath(f"//*[@id='blockAnimeNewArrive-{str(index)}']/div[2]/a/div[2]/div[2]")

    # 抓取動畫名稱
    names = block[0].xpath(".//p/text()")
    anime_name.extend([name.strip() for name in names if name.strip()])

    # 抓取集數
    episodes = block[0].xpath(".//div/span/text()")
    anime_episode.extend([episode.strip() for episode in episodes if episode.strip()])

    # 抓取年份
    years = block[0].xpath(".//div/p/text()")
    anime_year.extend([year.strip() for year in years if year.strip()])

    # 抓取URL
    urls = block[0].xpath(".//a/@href")
    anime_urls.extend(["https://ani.gamer.com.tw/" + url for url in urls if url])
'''



