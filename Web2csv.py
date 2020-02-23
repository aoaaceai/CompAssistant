import numpy as np
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup as BS


def search(string,start="", end=""):
    lstart=len(start)
    lend=len(end)
    startpoint=endpoint=0
    for i in range(len(string)):
        if string[i:i+lstart]==start:
            startpoint=i+lstart
    for i in range(len(string)-lend, startpoint, -1):
        if string[i:i+lend]==end:
            endpoint=i
    return string[startpoint:endpoint]

def _cd(name):
    if not os.path.isdir(name):
        os.mkdir(name)
    os.chdir(name)

def chd(name):
    for i in name.split('/'):
        _cd(i)
def savefile(Name, frame):
    chd('comps/'+Name)
    frame.to_csv('general.csv', index=False)
    pd.DataFrame(columns=['event', 'groupcount', 'overlaps with the next event (if so, type "1")', 'NOTE: If two events overlap, the time-consuming one should be on top of the faster one.']).to_csv('schedule.csv', index=False)

        
def cubingTW(Name=''):
    if Name=='':
        Name=input('input the comp name on the cubingTW:')
    pre_url='https://cubing-tw.net/event/'+Name+'/competitors'
    pre=requests.get(pre_url)
    presp=BS(pre.text,'html.parser')
    pre_list=presp.find('table').find('tfoot').find_all('tr')[1].find_all('th')
    event_list=[]
    for th in pre_list:
        result=th.find('span')
        if result!=None:
            event_list.append(search(str(result), 'title="', '"'))
    pre_list=presp.find('table').find('tbody').find_all('tr')
    frame=pd.DataFrame(np.empty((len(pre_list), len(event_list)+3), dtype=object), columns=['index', 'name', 'newbie']+event_list)
    for index, competitor in enumerate(pre_list):
        competitor=competitor.find_all('td')
        frame['index'][index]=int(competitor[0].text)
        frame['name'][index]=competitor[1].text
        for i, event in enumerate(competitor[5:]):
            if '-' not in event.text:
                try:
                    frame[event_list[i]][index]=1
                except IndexError: #if the registration isn't closed, another column will be added, causing this error
                    pass
        if competitor[2].text=="":
            frame['newbie'][index]=1
    savefile(Name, frame)
    return Name
def WCA(Name=''):
    if Name=='':
        Name=input('input the comp name on the WCA site:')
    pre_url='https://www.worldcubeassociation.org/competitions/'+Name+'/registrations'
    pre=requests.get(pre_url)
    presp=BS(pre.text,'html.parser')
    pre=presp.find('table')
    head=pre.find('thead').find_all('span')
    competitors=pre.find('tbody').find_all('tr')
    event_list=[]
    for i in head:
        event_list.append(i.attrs['title'])
    emp_list=np.empty((len(competitors), len(event_list)+3), dtype=object)
    frame=pd.DataFrame(emp_list, columns=['id', 'name', 'newbie']+event_list)
    for index, competitor in enumerate(competitors):
        competitor=competitor.find_all('td')
        name=competitor[0]
        if len(name.find_all('a'))==0:
            frame['newbie'][index]=1
        frame['name'][index]=name.text.strip()
        frame['id'][index]=index+1
        for i, event in enumerate(competitor[2:-2]):
            if len(event.find_all('span'))==0:
                continue
            frame[event_list[i]][index]=1
    savefile(Name, frame)
    return Name
if __name__=='__main__':
    WCA()
