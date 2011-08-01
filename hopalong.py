#! /usr/bin/env python

import pygame
import math

size = width,height = 800,600

pygame.init()
surface = pygame.display.set_mode( size )
surface.fill( (0, 0, 0) )

a = -55.0
b = -1.0
c = -42.0

x = 0.0
y = 0.0

colorvariance = 6000.0

def sign( x ):
	return 1.0 if x>=0 else -1.0

def plot( x, y, color ):
	surface.set_at( (int(x+width/2), int(y+height/2)), color )

def hsv_rgb( H, S, V ):
	H = math.fmod( H, 360.0 )

	hi = math.floor( H/60.0 )
	f = H/60.0-hi

	p = V*(1-S)
	q = V*(1-S*f)
	t = V*(1-S*(1-f))

	if hi == 0 or hi == 6:
		(R,G,B) = (V,t,p)
	elif hi == 1:
		(R,G,B) = (q,V,p)
	elif hi == 2:
		(R,G,B) = (p,V,t)
	elif hi == 3:
		(R,G,B) = (p,q,V)
	elif hi == 4:
		(R,G,B) = (t,p,V)
	else:
		(R,G,B) = (V,p,q)

	return (R,G,B)

def color( n ):
	(R,G,B) = hsv_rgb(
		n/colorvariance,
		1.0 * math.fabs( math.sin( n/478001.0 ) ),
		255.0 * math.fabs( math.sin( n/300000.0 ) ) )
	return (R,G,B)
	
iteration = 0
running = True
while running:

	surface.lock()
	for i in range( 1000 ):
		xx = y - sign( x ) * math.sqrt( math.fabs( b*x-c ) )
		y = a - x
		x = xx
		plot( x, y, color( iteration ) )
		iteration += 1
	surface.unlock()

	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = False

	pygame.display.flip()
