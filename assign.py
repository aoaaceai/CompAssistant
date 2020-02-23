import pandas as pd
import os
import numpy as np
import random
from string import ascii_uppercase as GROUPNAMES
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

def chunk(l, n):
    return list(map(np.ndarray.tolist, np.array_split(l, n)))

def check(person, event, group, group_dict):
    if person.newbie:
        return False
    if group_dict[event]<=2 and group not in person.judge[event] and group!=person.group[event]:
        return True
    if group==person.group[event] or group+1==person.group[event] or group in person.judge[event]:
        return False
    return True

def fill_group(e, group_size, gen, non_newbie, event_dict, group_dict, judges):
    global GROUPNAMES
    group_size[e]=[]
    for i, c in enumerate(chunk(event_dict[e], group_dict[e])):
        group_size[e].append(len(c))
        for p in c:
            gen[e][p.inner_id]=GROUPNAMES[i]
            p.group[e]=i
            if not p.newbie:
                non_newbie[e].append(p)
    judges[e]=[0]*group_dict[e]

def assign_judge(kid, e, m, judges, jud, group_dict):
    if check(kid, e, m, group_dict):
        global GROUPNAMES
        try:
            jud[e][kid.inner_id]+=GROUPNAMES[m]
        except:
            jud[e][kid.inner_id]=GROUPNAMES[m]
        kid.judge[e].append(m)
        judges[e][m]+=1
        return True
    else:
        return False

def fill_judge(e, non_newbie, group_dict, unlucky, judges, group_size, jud, overlap=0):
    global GROUPNAMES
    for p in non_newbie[e]:
        tmp=0 if p.group[e]==group_dict[e]-1 else p.group[e]+1
        p.judge[e]+=[tmp]
        jud[e][p.inner_id]=GROUPNAMES[tmp]
        judges[e][tmp]+=1
    random.shuffle(non_newbie[e])
    for m in range(group_dict[e]):
        while judges[e][m]<group_size[e][m]:
            for j, kid in enumerate(non_newbie[e]):
                if assign_judge(kid, e, m, judges, jud, group_dict):
                    unlucky[e].append(kid)
                    random.shuffle(non_newbie[e])
                    break
            else:
                for j, kid in enumerate(non_newbie['main']):
                    if (overlap==0 or check(kid, overlap, m, group_dict)) and assign_judge(kid, e, m, judges, jud, group_dict):
                        unlucky[e].append(kid)
                        non_newbie['main'].pop(j)
                        break
                else:
                    non_newbie['main']=non_newbie['backup'][:]
                    random.shuffle(non_newbie['main'])

def assign(name=''):
    if name=='':
        name=input('input the comp name on CubingTW:')
    os.chdir('comps/'+name)
    gen=pd.read_csv('general.csv')
    jud=pd.DataFrame(columns=gen.columns)
    jud['index']=gen['index']
    jud['name']=gen['name']
    schedule=pd.read_csv('schedule.csv')

    events=list(gen.columns[3:]) # a list of all the events
    people=[] # a list of all the competitors
    event_dict={} # consists of all the competitors in all events
    non_newbie={'main':[]} # simillar to event_dict, but all the competitors aren't newbies
    prev_overlap=False
    sch=[] # schedule of the comp, stored like [normal1, normal2, (overlap1, overlap2)] 
    group_dict={} # group counts of all the events 
    alias={'333': '3x3x3 Cube', '222': '2x2x2 Cube', '444': '4x4x4 Cube', '555': '5x5x5 Cube', '666':'6x6x6 Cube', 
    '777':'7x7x7 Cube','3x3x3 cube':'3x3x3 Cube','2x2x2 cube':'2x2x2 Cube','4x4x4 cube':'4x4x4 Cube','5x5x5 cube':'5x5x5 Cube',
    '6x6x6 cube':'6x6x6 Cube','7x7x7 cube':'7x7x7 Cube', '3x3x3 blindfolded':'3x3x3 Blindfolded', '3bld':'3x3x3 Blindfolded',
    '4x4x4 blindfolded':'4x4x4 Blindfolded', '4bld':'4x4x4 Blindfolded', '5x5x5 blindfolded':'5x5x5 Blindfolded', '5bld':'5x5x5 Blindfolded',
    'square-1':'Square-1', 'sq':'Square-1', 'pyraminx':'Pyraminx', 'pyra':'Pyraminx', 'megaminx':'Megaminx', 'mega':'Megaminx', 
    'skewb':'Skewb','sk':'Skewb', 'clock':'Clock', '3x3x3 multi-Blind':'3x3x3 Multi-Blind', 'mbld':'3x3x3 Multi-Blind', 
    '3x3x3 fewest moves':'3x3x3 Fewest Moves', 'fmc':'3x3x3 Fewest Moves', '3x3x3 one-handed':'3x3x3 One-Handed', 'oh':'3x3x3 One-Handed'}


    for i in schedule.index: # add stuff to sch
        schedule['event'][i]=alias[schedule['event'][i].lower()]
        if prev_overlap:
            sch[-1]=(schedule['event'][i-1], schedule['event'][i])
        else:
            sch.append(schedule['event'][i])
        group_dict[schedule['event'][i]]=int(schedule['groupcount'][i])
        if schedule['overlaps with the next event (if so, type "1")'][i]==1:
            prev_overlap=True
        else:
            prev_overlap=False

    for i in gen.index: # add stuff to event_dict and people, while assigning the group
        people.append(person())
        p=people[-1]
        p.id=gen['index'][i]
        p.name=gen['name'][i]
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
        p.newbie=gen['newbie'][i]==1
        jud['newbie'][i]=gen['newbie'][i]
        if not p.newbie:
            non_newbie['main'].append(p)
        p.inner_id=i

    non_newbie['backup']=non_newbie['main'][:]
    random.shuffle(non_newbie['main'])

    group_size={}
    judges={}
    unlucky={}
    for e in sch:
        print('Currently working:', e)
        unlucky[e]=[]
        if type(e)==str: #no overlap
            fill_group(e, group_size, gen, non_newbie, event_dict, group_dict, judges)
            fill_judge(e, non_newbie, group_dict, unlucky, judges, group_size, jud)

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
                fill_group(e, group_size, gen, non_newbie, event_dict, group_dict, judges)
                non_newbie[e]=[]
            for kid in overlapper:
                m=kid.group[e1]+1
                assign_judge(kid, e1, m, judges, jud, group_dict)
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
                        if assign_judge(kid, e1, m, judges, jud, group_dict):
                            non_newbie[e1].pop(index)
                            break
                    else:
                        for index, kid in enumerate(n1):
                            if assign_judge(kid, e1, m, judges, jud, group_dict):
                                unlucky[e1].append(kid)
                                break
                        else:
                            while True:
                                kid=random.choice(non_newbie['main'])
                                if e2 not in kid.event and assign_judge(kid, e1, m, judges, jud, group_dict):
                                    unlucky[e1].append(kid)
                                    break
            fill_judge(e2, non_newbie, group_dict, unlucky, judges, group_size, jud, overlap=e1)

    gen.to_csv('groups.csv', index=False)
    jud.to_csv('judge.csv', index=False)

if __name__=='__main__':
    assign()