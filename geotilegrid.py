# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 13:28:47 2021

@author: rohit
"""

#Rohit Rajuladevi rsr4qd
import pygame
import gamebox
import pandas as pd
import numpy as np


class Tile:
        x=0
        y=0
        name=''
        type='Tile'
        posx=0
        posy=0
class Space:
        x=0
        y=0
        type='Empty'
        posx=0
        posy=0



camerax=1200
cameray=800


global listoftiles
listoftiles=[]

df=pd.read_excel('Tilegrid1.xlsx', index_col=0)
pos=np.asarray(df['Position'])
names=np.asarray(df['NAMES'])

for i in range(len(pos)):
    pos[i]=pos[i].strip('[].').split()
    x=pos[i][0]
    x=x.replace('.',"")
    x=x.replace(',',"")
    pos[i][0]=x

    pos[i][0]=int(pos[i][0])
    y=pos[i][1]
    y=y.replace('.',"")
    y=y.replace(',',"")
    pos[i][1]=y
    pos[i][1]=int(pos[i][1])


    

xm=0
ym=0
for i in pos:
    if(i[0]>xm):
        xm=i[0]
    if(i[1]>ym):
        ym=i[1]

gridsize=[xm+1,ym+1]

stepx=(camerax//(gridsize[0]+1))
tileszx=(stepx-10)

stepy=(cameray//(gridsize[1]+1))
tileszy=(stepy-10)

startingx=tileszx+5
startingy=tileszy+5






camera=gamebox.Camera(camerax,cameray)



for j in range(gridsize[1]):
    for i in range(gridsize[0]):
        result = any(elem == [i,j] for elem in pos)
        
        if result:
            box=gamebox.from_color(startingx + stepx*i,startingy + stepy*j,'black',tileszx,tileszy)
            text=names[pos.tolist().index([i,j])]
            t=Tile()
            t.name=text
            t.x=startingx + stepx*i
            t.y=startingy + stepy*j
            t.posx=i
            t.posy=j
            listoftiles.append(t)
        else:
            s=Space()
            s.x=startingx + stepx*i
            s.y=startingy + stepy*j
            s.posx=i
            s.posy=j
            listoftiles.append(s)

        
global switchls
switchls=[]

restart=False

dwn=False
lft=False

def tick(keys):
    global restart
    global listoftiles
    global tileszx
    global tileszy
    global names
    global dwn
    global lft

    camera.clear('white')
    if(restart):

        listoftiles=[]
        df=pd.read_excel('Tilegrid1.xlsx', index_col=0)
        pos=np.asarray(df['Position'])
        names=np.asarray(df['NAMES'])

        for i in range(len(pos)):
            pos[i]=pos[i].strip('[].').split()
            x=pos[i][0]
            x=x.replace('.',"")
            x=x.replace(',',"")
            pos[i][0]=x

            pos[i][0]=int(pos[i][0])
            y=pos[i][1]
            y=y.replace('.',"")
            y=y.replace(',',"")
            pos[i][1]=y
            pos[i][1]=int(pos[i][1])


            

        xm=0
        ym=0
        for i in pos:
            if(i[0]>xm):
                xm=i[0]
            if(i[1]>ym):
                ym=i[1]
        if(dwn):
            gridsize=[xm+1,ym+2]
            dwn=False
        elif(lft):
            gridsize=[xm+2,ym+1]
            lft=False
        else:
            gridsize=[xm+1,ym+1]


        stepx=(camerax//(gridsize[0]+1))
        tileszx=(stepx-10)

        stepy=(cameray//(gridsize[1]+1))
        tileszy=(stepy-10)

        startingx=tileszx+5
        startingy=tileszy+5

                
        for j in range(gridsize[1]):
            for i in range(gridsize[0]):
                result = any(elem == [i,j] for elem in pos)
                
                if result:
                    box=gamebox.from_color(startingx + stepx*i,startingy + stepy*j,'black',tileszx,tileszy)
                    text=names[pos.tolist().index([i,j])]
                    t=Tile()
                    t.name=text
                    t.x=startingx + stepx*i
                    t.y=startingy + stepy*j
                    t.posx=i
                    t.posy=j
                    listoftiles.append(t)
                else:
                    s=Space()
                    s.x=startingx + stepx*i
                    s.y=startingy + stepy*j
                    s.posx=i
                    s.posy=j
                    listoftiles.append(s)
        restart=False
                        

                
    
    
          
    for i in listoftiles:
        if(i.type=='Tile'):
            camera.draw(gamebox.from_color(i.x,i.y,'black',tileszx,tileszy))
            camera.draw(gamebox.from_text(i.x,i.y, i.name, 12, 'yellow', bold=False, italic=False))
        else:
            camera.draw(gamebox.from_color(i.x,i.y,'blue',tileszx,tileszy))
        


        k=gamebox.from_color(i.x,i.y,'blue',tileszx,tileszy)

        if(k.contains(camera.mouse) and camera.mouseclick):


            switchls.append(i)

            
            try:
                if(switchlss[0] in switchls or switchlss[1] in switchls):
                    switchls.clear()
            except:
                pass

                
            
            if(len(set(switchls))==2):
                switchlss=list(set(switchls))
                listoftiles.remove(switchlss[0])
                listoftiles.remove(switchlss[1])
                tempx=switchlss[0].x
                tempy=switchlss[0].y
                temppx=switchlss[0].posx
                temppy=switchlss[0].posy
                
                switchlss[0].x=switchlss[1].x
                switchlss[0].y=switchlss[1].y
                switchlss[0].posx=switchlss[1].posx
                switchlss[0].posy=switchlss[1].posy

                switchlss[1].x=tempx
                switchlss[1].y=tempy
                switchlss[1].posx=temppx
                switchlss[1].posy=temppy
                listoftiles.append(switchlss[0])
                listoftiles.append(switchlss[1])

                names=[]
                positions=[]

                for i in listoftiles:
                    if(i.type=='Tile'):
                        names.append(i.name)
                        positions.append('['+str(i.posx)+', '+str(i.posy)+']')
                        df1=pd.DataFrame()
                        df1['NAMES']=np.asarray(names)
                        df1['Position']=np.asarray(positions)
                        df1.to_excel('Tilegrid1.xlsx')
                restart=True
                    

                switchls.clear()

    if pygame.K_UP in keys:
        names=[]
        positions=[]
        for i in listoftiles:
            if(i.type=='Tile'):
                names.append(i.name)
                positions.append('['+str(i.posx)+', '+str(i.posy+1)+']')
                df1=pd.DataFrame()
                df1['NAMES']=np.asarray(names)
                df1['Position']=np.asarray(positions)
                df1.to_excel('Tilegrid1.xlsx')
        restart=True
    if pygame.K_DOWN in keys:
        dwn=True
        restart=True

    if pygame.K_LEFT in keys:
        names=[]
        positions=[]
        for i in listoftiles:
            if(i.type=='Tile'):
                names.append(i.name)
                positions.append('['+str(i.posx+1)+', '+str(i.posy)+']')
                df1=pd.DataFrame()
                df1['NAMES']=np.asarray(names)
                df1['Position']=np.asarray(positions)
                df1.to_excel('Tilegrid1.xlsx')
        restart=True

    if pygame.K_RIGHT in keys:
        lft=True
        restart=True


    camera.display()







gamebox.timer_loop(30, tick)




names=[]
positions=[]
minx=9999999
miny=9999999

for i in listoftiles:
    if(i.type=='Tile'):
        if(minx>i.posx):
            minx=i.posx
        if(miny>i.posy):
            miny=i.posy

for i in listoftiles:
    if(i.type=='Tile'):
        names.append(i.name)
        positions.append('['+str(i.posx-minx)+', '+str(i.posy-miny)+']')
names=np.asarray(names)
positions=np.asarray(positions)
df1=pd.DataFrame()
df1['NAMES']=names
df1['Position']=positions
df1.to_excel('Tilegrid1.xlsx')
    









