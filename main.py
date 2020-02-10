import pandas as pd
import os
import numpy as np
import random
from string import ascii_uppercase as GROUPNAMES
os.chdir(input('請輸入cubingTW上的比賽英文名:'))
gen=pd.read_csv('general.csv')
jud=pd.DataFrame(columns=gen.columns)
jud['編號']=gen['編號']
jud['姓名']=gen['姓名']
schedule=pd.read_csv('schedule.csv')
GROUPNAMES=list(GROUPNAMES)
class person:
    def __init__(self, id='0', name='example', event=[], newbie=True, inner_id=0):
        self.id=id
        self.name=name
        self.event=event
        self.newbie=newbie
        self.inner_id=inner_id
        self.group={}
        self.judge={}
    def __str__(self):
        return "id:{}\nname:{}\nevents:{}\nnewbie:{}\ngrouping:{}\njudge:{}".format(self.id, self.name, self.event, self.newbie, self.group, self.judge)
events=list(gen.columns[3:])
people=[]
event_dict={}
non_newbie={'main':[]}
prev_overlap=False
sch=[]
group_dict={}
for i in schedule.index:
    if prev_overlap:
        sch[-1]=(schedule.項目[i-1], schedule.項目[i])
    else:
        sch.append(schedule.項目[i])
    group_dict[schedule.項目[i]]=int(schedule.組數[i])
    if schedule['是否與下個賽程重疊(有的話請輸入1)'][i]==1:
        prev_overlap=True
    else:
        prev_overlap=False
for i in gen.index:
    people.append(person())
    p=people[-1]
    p.id=gen.編號[i]
    p.name=gen.姓名[i]
    event=[]
    for e in events:
        if gen[e][i]==1:
            event.append(e)
            if e not in event_dict:
                event_dict[e]=[]
                non_newbie[e]=[]
            event_dict[e].append(p)
        p.group[e]=-1
        p.judge[e]=[]
    p.event=event
    p.newbie=gen.新手[i]==1
    jud.新手[i]=gen.新手[i]
    if not p.newbie:
        non_newbie['main'].append(p)
    p.inner_id=i
non_newbie['backup']=non_newbie['main'][:]
random.shuffle(non_newbie['main'])
def chunk(l, n):
    return list(map(np.ndarray.tolist, np.array_split(l, n)))
def check(person, event, group):
    global group_dict
    if person.newbie:
        return False
    if group_dict[e]<=2 and group not in person.judge[event] and group!=person.group[event]:
        return True
    if group==person.group[event] or group+1==person.group[event] or group in person.judge[event]:
        return False
    return True
def fill_group(e):
    global group_size, gen, GROUPNAMES, non_newbie
    group_size[e]=[]
    for i, c in enumerate(chunk(event_dict[e], group_dict[e])):
        group_size[e].append(len(c))
        for p in c:
            gen[e][p.inner_id]=GROUPNAMES[i]
            p.group[e]=i
            if not p.newbie:
                non_newbie[e].append(p)
    judges[e]=[0]*group_dict[e]
def assign_judge(kid, e, m):
    if check(kid, e, m):
        global jud, GROUPNAMES
        try:
            jud[e][kid.inner_id]+=GROUPNAMES[m]
        except:
            jud[e][kid.inner_id]=GROUPNAMES[m]
        kid.judge[e].append(m)
        judges[e][m]+=1
        return True
    else:
        return False
def fill_judge(e, overlap=0):
    global non_newbie, group_dict, unlucky, judges, group_size, GROUPNAMES
    for p in non_newbie[e]:
        tmp=0 if p.group[e]==group_dict[e]-1 else p.group[e]+1
        p.judge[e]+=[tmp]
        jud[e][p.inner_id]=GROUPNAMES[tmp]
        judges[e][tmp]+=1
    random.shuffle(non_newbie[e])
    for m in range(group_dict[e]):
        while judges[e][m]<group_size[e][m]:
            for j, kid in enumerate(non_newbie[e]):
                if assign_judge(kid, e, m):
                    unlucky[e].append(kid)
                    random.shuffle(non_newbie[e])
                    break
            else:
                for j, kid in enumerate(non_newbie['main']):
                    if (overlap==0 or check(kid, overlap, m)) and assign_judge(kid, e, m):
                        unlucky[e].append(kid)
                        non_newbie['main'].pop(j)
                        break
                else:
                    non_newbie['main']=non_newbie['backup'][:]
                    random.shuffle(non_newbie['main'])
group_size={}
judges={}
unlucky={}
for e in sch:
    print('Currently working:', e)
    unlucky[e]=[]
    if type(e)==str: #no overlap
        fill_group(e)
        fill_judge(e)
    else: #overlap
        pass
        e1, e2=e
        unlucky[e1]=[]
        unlucky[e2]=[]
        good=([],[])
        overlapper=[]
        for p in event_dict[e1]:
            if e2 in p.event:
                overlapper.append(p)
            else:
                good[0].append(p)
        for p in event_dict[e2]:
            if e1 not in p.event:
                good[1].append(p)
        event_dict[e1]=overlapper+good[0]
        event_dict[e2]=good[1]+overlapper
        for e in (e1, e2):
            fill_group(e)
            non_newbie[e]=[]
        for kid in overlapper:
            m=kid.group[e1]+1
            assign_judge(kid, e1, m)
        for p in good[0]:
            if not p.newbie:
                non_newbie[e1].append(p)
        for p in good[1]:
            if not p.newbie:
                non_newbie[e2].append(p)
        n1=non_newbie[e1][:]
        for m in range(group_dict[e1]):
            while judges[e1][m]<group_size[e1][m]:
                for index, kid in enumerate(non_newbie[e1]):
                    if assign_judge(kid, e1, m):
                        non_newbie[e1].pop(index)
                        break
                else:
                    for index, kid in enumerate(n1):
                        if assign_judge(kid, e1, m):
                            unlucky[e1].append(kid)
                            break
                    else:
                        while True:
                            kid=random.choice(non_newbie['main'])
                            if e2 not in kid.event and assign_judge(kid, e1, m):
                                unlucky[e1].append(kid)
                                break
        fill_judge(e2, overlap=e1)

gen.to_csv('group.csv', index=False)
jud.to_csv('judge.csv', index=False)
