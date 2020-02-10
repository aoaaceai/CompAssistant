CompAssistant
=
An automatic grouping system that assigns everyone's group and judges for cubing comps. 
Currently works for Taiwanese comps since it grabs data from [CubingTW](https://cubing-tw.net). But if you already have data from competitors, [main.py](./main.py) can still do its job.

## Requirements
- python3 with the following modules installed:
    - numpy
    - pandas
    - requests
    - bs4

## Using this tool
1. Find the *English* name of the comp at [CubingTW](https://cubing-tw.net). For example, *2019CKCubingParty* for *Chien Kuo Cubing Party 2019*. If the name is correct, you should see the info page of that comp at cubing-tw.net/event/*COMP_NAME*.
2. Run [Web2csv.py](./Web2csv.py) and paste the comp name if it asks to.
3. You should find a new folder created, containing *general.csv* and *schedule.csv*.
4. in *schedule.csv*, type in the schedule of that comp. Make sure you follow the instructions in that file. the  alias of some event names are listed below:


    | Event name | alias |
    | -------- | -------- |
    | *n*x*n*x*n* Cube | *nnn* |
    | Pyraminx | pyra |
    | Megaminx | mega |
    | Square-1 | sq |
    | Skewb | sk |
    | *n*x*n*x*n* Blindfolded| *n*bld |
    | 3x3x3 Multi-Blind | mbld|
    | 3x3x3 Fewest Moves | fmc|
    | 3x3x3 One-Handed | oh|
    | 3x3x3 With Feet | **FEET IS NO LONGER AN EVENT**|
    | Clock | clock | 
    
5. In *general.csv*, you can decide whether a competitor will become a judge or not. Since only the non-newbies will be the judges, comp organizers and delegates can be viewed as a newbie. Just set their *newbie* value to 1. Also, if a newbie is familliar with the regulations and willing to be a judge, set their *newbie* value to nothing.
6. Run [main.py](./main.py), and paste the comp name if it asks to.
7. You should find two more new files in the folder, respectively *groups.csv* for the comp grouping and *judge.csv* for their judge duty.

## Notice
I suck at programming. If you've find any bugs, please report them at the *issue* section, or make a pull request if you're kind enough to do so.
