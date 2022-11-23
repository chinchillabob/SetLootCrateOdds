import pandas as pd
import random 
import matplotlib as plt
import numpy as np
from tkinter import *

#show the variance and number of crates to converge


def square(cards):
    n = cards[0]
    v = cards[1]**2
    return(n , v)

#return softmax list of length = num cards
def init_p(cards):
    p = 1.0
    p_list = []
    i  = 0 
    while i < len(cards):
        if i == (len(cards) - 1):
            p_list.append(p)
        else:
            r = p / 2
            p = p - r
            p_list.append(r)
        i = i + 1
    return p_list

#expected value
def ev(cards, p):
    value = 0
    i = 0
    while i < len(p):
        value = value + (cards[i][1] * p[i])
        i = i + 1
    return value

def redistributeDelta(sum_delta, p_0, p_1, cards, v, win_rate):
    distribTo = np.zeros(len(p_0), dtype=int).tolist()
    i = 0
    while i < len(p_0):
        if(ev(cards, p_0) > v*win_rate):
            if(v>cards[i][1]>0):
                distribTo[i] = 1
        else:
            if(cards[i][1] >= v*win_rate):
                distribTo[i] = 1
        i = i + 1
    n = distribTo.count(1)
    i = 0
    v_to_red = sum_delta/n
    while i < len(p_1):
        if distribTo[i] == 1:
            p_1[i] += v_to_red
        i = i + 1
    return p_1



#v = crate price
def update_p(p_0, cards, v, learning_rate, win_rate):
    p_1 = p_0.copy()
    i = 0
    sum_delta = 0
    t_0_ev = ev(cards, p_0)
    while i < len(p_0):
        if(t_0_ev > v*win_rate) :
            if(cards[i][1] >= v*win_rate): #added winrate to if statement
                p_1[i] = p_1[i] - learning_rate
                sum_delta += learning_rate
        else:
            if(cards[i][1] <= v*win_rate): #added winrate to if statement
                p_1[i] = p_1[i] - learning_rate
                sum_delta += learning_rate
        i = i + 1
    p_1 = redistributeDelta(sum_delta, p_0, p_1, cards, v, win_rate)
    return p_1
    


#value = crate price
#cards matrix which contains v_i
#v_i value of card i
def odds(value, cards, learning_rate, max_iter, win_rate):
    #p list of probabilities with a one to one relationship with the number of cards
    p = init_p(cards)
    i = 0
    while i < max_iter:
        squared_loss = (ev(cards, p) - (value*win_rate))**2
        if learning_rate>squared_loss**0.5:
            print(f"steps to converge: {i }")
            return p
        else:
            p = update_p(p, cards, value,  learning_rate, winrate)
        i = i + 1
    return p

#for any crate price
cratePrice = 3.5
#add any amount of cards
cards = [('c1', 1), ('c2', 2), ('c3', 3), ('c4', 4), ('c5', 5), ('c6', 10)]
#winrate =0.9 means that the ev for the house should be 10% of the cost of the crate
winrate=0.9
new_p = odds(cratePrice, cards, 0.001, 900, winrate)
print(new_p)
print(cratePrice*winrate)
print(ev(cards, new_p))
