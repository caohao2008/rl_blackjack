#!/bin/python
import os
import sys
import random

def judgeTerminate(a,b):
    if(len(a)==0 or len(b)==0):
        return 0
    elif len(a)>=3 or len(b)>=3:
        return 1
    else:
        return 0

def draw(a,b):
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       a.append(int(random.random()*100)%11+1)
     
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       b.append(int(random.random()*100)%11+1)
    return a,b

def judgeWin(a,b):
    avalue = 0
    bvalue = 0
    for k in a:
        avalue = avalue+k
    for l in b:
        bvalue = bvalue+l
    if((avalue>21 and bvalue>21) or (avalue==bvalue)):
        return 0
    elif(avalue>21 and bvalue<=21):
        return -1
    elif(avalue<=21 and bvalue>21):
        return 1
    elif(avalue<=21 and bvalue<=21):
        if(avalue>bvalue):
            return 1
        else:
            return -1
    else:
        print("error")
        return -2


def make_current_status(a,b):
    status = []
    status_str = ""+str(b[0])+"-"
    for s in a:
        status_str=status_str+str(s)+"_"
    return status_str



def make_status(a,b):
    status = []
    status_str = ""+str(b[0])+"-"
    for s in a:
        status_str=status_str+str(s)+"_"
        status.append(status_str)
    return status

ns={}


def double_update(a,b,mdp):
    update(a,b,mdp)
    update(b,a,mdp)

def update(a,b,mdp):
    statuses = make_status(a,b)
    cnt=0
    for s in statuses:
        if(cnt==len(statuses)-1):
            s_a=s+"n"
        else:
            s_a=s+"y"    
        if not ns.has_key(s_a):
            ns[s_a]=0
            mdp[s_a]=0
        ns[s_a]=ns[s_a]+1
        mdp[s_a]=((ns[s_a]-1)*mdp[s_a]+judgeWin(a,b))/float(ns[s_a])
        cnt=cnt+1
       
mdp={}

def draw_with_model(a,b,mdp):
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       b.append(int(random.random()*100)%11+1)
   
    if(len(b)==0):
        return a,b
        
    a_s = make_current_status(a,b)
    a_s_y = a_s+"y"
    a_s_n = a_s+"n" 
    a_s_a_y = 0
    a_s_a_n = 0
    if mdp.has_key(a_s_y): 
        a_s_a_y =  mdp[a_s_y]
    
    if mdp.has_key(a_s_n): 
        a_s_a_n =  mdp[a_s_n]
    #print a_s+","+"y:"+str(a_s_a_y)+",n:"+str(a_s_a_n)
    if(a_s_a_y>=a_s_a_n):
        a.append(int(random.random()*100)%11+1)
    
    return a,b

def sum(a):
    result=0
    for r in a:
        result=result+r
    return result

def draw_with_rule(a,b,mdp):
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       b.append(int(random.random()*100)%11+1)
   
    a_sum=sum(a)
    if(a_sum<11):
        a.append(int(random.random()*100)%11+1)

    return a,b



def play_loop(mode): 
    ping=lose=win=0
    for i in range(1,100000):
        a=[]
        b=[]
        while(not judgeTerminate(a,b)):
            #draw pocket
            if(mode=='train'):
                a,b = draw(a,b)
            elif(mode=='mc'):
                a,b = draw_with_model(a,b,mdp)
            elif(mode=='rule'):
                a,b = draw_with_rule(a,b,mdp)
        

        #print("a="+str(a)+" b="+str(b)+"\t"+str(judgeWin(a,b)) )
        if(judgeWin(a,b)==0):
            ping=ping+1
        elif(judgeWin(a,b)==-1):
            lose=lose+1
        else:
            win=win+1 
        #update(a,b,mdp)
        double_update(a,b,mdp)
        #print(i)
    print "total : win =",win,", lose =",lose," tie=",ping


    #for s in mdp:
        #print s,ns[s],mdp[s]

def play_with_mdp():
    a=[]
    b=[]
    b_value = raw_input("please input b\n")
    b.append(int(b_value))
    a_value = raw_input("please input a\n")
    a.append(int(a_value))
    while(1):
        a_s = make_current_status(a,b)
        a_s_y = a_s+"y"
        a_s_n = a_s+"n" 
        a_s_a_y = 0
        a_s_a_n = 0
        if mdp.has_key(a_s_y): 
            a_s_a_y =  mdp[a_s_y]
    
        if mdp.has_key(a_s_n): 
            a_s_a_n =  mdp[a_s_n]
        print a_s+","+"y:"+str(a_s_a_y)+",n:"+str(a_s_a_n)
        if(sum(a)>21):
            print "lose!"
            break
        if(a_s_a_y>=a_s_a_n):
            print "draw!"
            a_value = raw_input("please input a\n")
            a.append(int(a_value))
        else:
            print "stop!"
            break


play_loop('train')
play_loop('rule')
play_loop('mc')

#use mdp to play!
while(1):
    play_with_mdp()
