#!/bin/python
import os
import sys
import random

def judgeTerminate(a,b):
    if len(a)>=3 or len(b)>=3:
        return 1
    elif sum(a)>21 and sum(b)>21:
        return 1
    else:
        return 0

def init_draw(a,b):
    a.append(rand_draw())
    b.append(rand_draw())
    return a,b


def rand_draw():
    res = int(random.random()*100)%14+1
    if res>=11:
        res = 10
    return res
 

def draw(a,b):
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       a.append(rand_draw())
     
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       b.append(rand_draw())
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
       b.append(rand_draw())
   
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
        a.append(rand_draw())
    
    return a,b

def sum(a):
    result=0
    for r in a:
        result=result+r
    return result

def draw_with_rule(a,b,mdp):
    yes_or_no=random.random()
    if(yes_or_no<0.5):
       b.append(rand_draw())
   
    a_sum=sum(a)
    if(a_sum<11):
        a.append(rand_draw())

    return a,b



def play_loop(mode): 
    ping=lose=win=0
    for i in range(1,100000):
        a=[]
        b=[]
        a,b = init_draw(a,b)
        while(not judgeTerminate(a,b)):
            #draw pocket
            if(mode=='train'):
                a,b = draw(a,b)
            elif(mode=='mc'):
                a,b = draw_with_model(a,b,mdp)
            elif(mode=='rule'):
                a,b = draw_with_rule(a,b,mdp)
            elif(mode=='self-play'):
                a,b = self_play_with_mdp()  
        	#print("a="+str(a)+" b="+str(b)+"\t"+str(judgeWin(a,b)) )

        #print("a="+str(a)+" b="+str(b)+"\t"+str(judgeWin(a,b)) )
        if(judgeWin(a,b)==0):
            ping=ping+1
        elif(judgeWin(a,b)==-1):
            lose=lose+1
        else:
            win=win+1 
        update(a,b,mdp)
        #double_update(a,b,mdp)
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

def self_play_with_mdp():
    a=[]
    b=[]
    a,b = init_draw(a,b)
    a_stop=b_stop=0
    lunshu=0
    while(1):
        #a decision
        a_s = make_current_status(a,b)
        a_s_y = a_s+"y"
        a_s_n = a_s+"n" 
        a_s_a_y = 0
        a_s_a_n = 0
        if mdp.has_key(a_s_y): 
            a_s_a_y =  mdp[a_s_y]
    
        if mdp.has_key(a_s_n): 
            a_s_a_n =  mdp[a_s_n]
        ##print a_s+","+"y:"+str(a_s_a_y)+",n:"+str(a_s_a_n)
        if(a_s_a_y>=a_s_a_n and sum(a)<21):
            ##print "draw!"
            a_value = rand_draw()
            a.append(int(a_value))
        else:
            a_stop = 1
            ##print "a stop!"
        
        #b decision
        b_s = make_current_status(b,a)
        b_s_y = b_s+"y"
        b_s_n = b_s+"n" 
        b_s_b_y = 0
        b_s_b_n = 0
        if mdp.has_key(b_s_y): 
            b_s_b_y =  mdp[b_s_y]
    
        if mdp.has_key(b_s_n): 
            b_s_b_n =  mdp[b_s_n]
        ##print b_s+","+"y:"+str(b_s_b_y)+",n:"+str(b_s_b_n)
        if(b_s_b_y>=b_s_b_n and sum(b)<21):
            ##print "b draw!"
            b_value = rand_draw()
            b.append(int(b_value))
        else:
            b_stop = 1
            ##print "b stop!"
        
        if(a_stop==1 and b_stop==1):
            ##print "stop!"
            break
    return a,b


play_loop('train')
play_loop('rule')
play_loop('mc')
play_loop('self-play')
play_loop('mc')

#use mdp to self play!
#for i in range(1,1000):
#    a,b = self_play_with_mdp()

#    print("a="+str(a)+" b="+str(b)+"\t"+str(judgeWin(a,b)) )


#use mdp to play!
#while(1):
#    play_with_mdp()
