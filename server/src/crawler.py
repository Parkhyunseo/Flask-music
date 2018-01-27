from __future__ import unicode_literals
import re
import requests
from bs4 import BeautifulSoup
import csv

"""
1. http://www.melon.com/chart/index.htm에서 인기순위 50위 까지 긁어온다.
2. 차트를 보여준다 [어떻게 할지 고민]
3. http://www.melon.com/song/detail.htm?songId= 에서 디테일 정보를 가져온다.
4. 디테일 정보에는 장르, 그룹이름, 가사 등이 있다.
5. 장르로 Donut Charts
6. 가사로 Word Cloud
"""
def melon_chart():
    chart_url = 'http://www.melon.com/chart/index.htm'
    
    # User-Agent를 넘겨주니까 된다.
    headers = {
        "Accept-Language": "ko",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1;)"
    }
    
    result = requests.get(chart_url, headers=headers)
    print(result.content)
    print(result.reason)
    print(result.text)
    print(result.url)
    
    #html = requests.get(chart_url).text
    soup = BeautifulSoup(result.text, 'html.parser')
    melon_list = []
    
    with open('../../static/csv/melon.csv','w') as csvFile:
        fieldnames = ['idx', 'tag', 'url']
        csv_writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        csv_writer.writeheader()
    
        print(soup.select('#tb_list'))
        for idx, song_tag in enumerate(soup.select('#tb_list .lst50 a[href*=playSong]'), 1):
            print(idx)
            menu_id, song_id = re.findall(r'\d+', song_tag['href'])
            song_url = 'http://www.melon.com/song/detail.htm?songId=' + song_id
            if idx <= 4:
                csv_writer.writerow({'idx': 240000-(idx*40000), 'tag': song_tag.text, 'url': song_url})
            else:
                csv_writer.writerow({'idx': 50000-(500*idx - idx*idx), 'tag': song_tag.text, 'url': song_url})
            melon_list.append((song_tag.text, song_url))
            print(idx, song_tag.text, '||', song_url)
        
    return melon_list

melon_chart()