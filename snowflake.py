#!/usr/bin/env python

import turtle as t
import math
from time import sleep

# custom values
n = 23
sz = 300


def snowflake(radius, iter, anti):
    n = 3   # number of sides
    side_length = radius * math.sqrt(3)
    angle = (360 / 2) - (60 / 2)

    t.fd(radius)        # forward
    t.rt(angle)         # right turn

    for i in range(n):
        f(side_length, iter, anti)
        t.rt(360 / n)

    t.rt(-angle)
    t.bk(radius)        # backward


def f(length, depth, anti):
    if depth == 0:
        t.pd()          # pendown
        t.fd(length)    # forward
        t.pu()          # penup
        return

    for angle in [60, -120, 60, 0]:
        f(length/3, depth-1, anti)
        t.lt(angle * anti)


# main
t.reset()
t.speed(0)          # fast++
t.ht()              # hideturtle
t.pu()              # penup
screen = t.getscreen()
screen.bgcolor("black")
sleep(1)

for i in range(n):
    screen.tracer(49152, 0) # i
    # a b/w version
    cl = float(i+2) / float(n+2)
    t.color((cl, cl, cl))

    t.fill(True)        # 
    snowflake(sz, 5, 1) # i+2
    sz = sz - (sz / 8)  #
    t.fill(False)       #

t.mainloop()
