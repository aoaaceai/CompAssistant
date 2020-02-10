import numpy as np
import requests
import pandas as pd
import textsearch
import os
from bs4 import BeautifulSoup as BS
def web2csv(Name=''):
    if Name=='':
        Name=input('請輸入CubingTW的比賽英文名')
    pre_url='https://cubing-tw.net/event/'+Name
    pre=requests.get(pre_url+'/competitors')
    presp=BS(pre.text,'html.parser')
    pre_list=presp.find('table').find('tfoot').find_all('tr')[1].find_all('th')
    event_list=[]
    for th in pre_list:
        result=th.find('span')
        if result!=None:
            event_list.append(textsearch.search(str(result), 'title="', '"'))
    pre_list=presp.find('table').find('tbody').find_all('tr')
    frame=pd.DataFrame(np.empty((len(pre_list), len(event_list)+3), dtype=object), columns=['編號', '姓名', '新手']+event_list)
    for index, competitor in enumerate(pre_list):
        competitor=competitor.find_all('td')
        frame['編號'][index]=int(competitor[0].text)
        frame['姓名'][index]=competitor[1].text
        for i, event in enumerate(competitor[5:]):
            if '-' not in event.text:
                frame[event_list[i]][index]=1
        if competitor[2].text=="":
            frame['新手'][index]=1
    try:
        os.chdir(Name)
    except FileNotFoundError:
        os.mkdir(Name)
        os.chdir(Name)
    frame.to_csv('general.csv', index=False)
    pd.DataFrame(columns=['項目', '組數', '是否與下個賽程重疊(有的話請輸入1)', 'NOTE: 如果有重疊賽程的話，請把費時項目放在快速項目上面']).to_csv('schedule.csv', index=False)
    return Name

if __name__=='__main__':
    web2csv()
