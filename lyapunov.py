#!/usr/bin/env python

# Single best explanation: http://plus.maths.org/content/extracting-beauty-chaos

import sys
from time import sleep
from time import time as unixtime
import math
import tools.window as window
from threading import Thread
import signal


try:
	import pycuda.gpuarray as gpuarray
	import pycuda.driver as cuda
	import pycuda.autoinit
	import numpy
	pycuda_loaded = True 
except ImportError: 
	pycuda_loaded = False 


# fractal parameters
S = "AABAB"
(xmin, ymin) = (0.0, 0.0)
(xmax, ymax) = (4.0, 4.0)

# default window size
# height set automatically
window_width = 300      #  -- ( 200 )
window_aspect = 1.     #  -- ( 1.0 )

# accuracy
limes_precision = 0.05  #  -- ( 0.05 )
N_min = 30
N_max = 10000

def sign( x ):
	return 1.0 if x>=0 else -1.0

def color_linear_red_white( x ):
	if x > 0.7:
		return (255,255,255)
	if x > -1.0:
		c = int( ( x + 1.0 ) / 1.7 * 255 )
		return (255,c,c)
	if x > -4.0:
		c = int( ( x + 4.0 ) / 3.0 * 255 )
		return (c,0,0)
	else:
		return (0,0,0)

def color_exponential_red_white_blue( x ):
	T = 0.7 - x + 1.0
	if T < 1.0:
		T = 1.0
	T = 1.0 - 1.0 / T
	T = (T*0.92)**.15
	R = int(T*255**(1-T**45*2))
	G = int(T*70-880*T**18+701*T**9)
	B = int(T*80+T**9*255-950*T**99)
	R = 0 if R<0 else R
	R = 255 if R>255 else R
	G = 0 if G<0 else G
	G = 255 if G>255 else G
	B = 0 if B<0 else B
	B = 255 if B>255 else B
	return (R,G,B)

def color_plain_exponent( x ):
	T = 0.7 - x + 1.0
	if T < 1.0:
		T = 1.0
	T = 1.0 / T
	T = int( T*255 )
	T = 0 if T<0 else T
	T = 255 if T>255 else T
	return (T,T,T)

color_schemes = [
	color_exponential_red_white_blue,
	color_linear_red_white,
	color_plain_exponent,
]

def r( n, a, b ):
	if S[n % len(S)] == 'A':
		return a
	else:
		return b

def L_exp( a, b ):
	x_n = 0.5
	sum = 0.0

	for n in xrange( 1, N_min ):
		r_tmp = r( n, a, b )
		x_n = r_tmp * x_n * ( 1 - x_n )
		fa = math.fabs( r_tmp * ( 1 - 2*x_n ) )

		if fa > 0:
			diff = math.log( fa )
		else:
			diff = -40.0

		sum += diff
		
	for n in xrange( N_min, N_max ):
	    r_tmp = r( n, a, b )
	    x_n = r_tmp * x_n * ( 1 - x_n )
	    fa = math.fabs( r_tmp * ( 1 - 2*x_n ) )
	    
	    if fa > 0:
	        diff = math.log( fa )
	    else:
	        diff = -40.0
	
	    sum += diff
	    if math.fabs( diff/n ) < limes_precision:
	        break
	
	return sum/n

class Render( Thread ):

	def __init__( self, window ):
		#super(Thread, self).__init__()
		Thread.__init__( self )
		self.window = window
		self._stop = False

	def run( self ):
		self.render_window()

	def stop( self ):
		self._stop = True

	def finish( self ):
		self.stop()
		self.join()

	def render_window( self ):
		for (pixel, coord) in self.window if not render_random else self.window.random():
			e = L_exp( *coord )
			self.window.plot( pixel, color_schemes[color_scheme](e) )
			if self._stop:
				return

def quit_handler( signal, frame ):
	if job:
		job.finish()
	sys.exit( 0 )

signal.signal( signal.SIGINT, quit_handler )

render_random = True
state = 'resize'
win = False
job = False
color_scheme = 0

while True:

	if state == 'resize':
		if job:
			job.finish()
		win = window.Window( window_width, window_aspect, (xmin, ymin), (xmax, ymax) )
		win.set_title( 'Lyapunov' )
		state = 'render'
	elif state == 'render':
		job = Render( win )
		job.start()
		state = 'rendering'
	elif state == 'rendering':
		if not job.is_alive():
			state = 'idle'
	elif state == 'idle':
		job = False
	elif state == 'quit':
		if job:
			job.finish()
		sys.exit( 1 )

	if win:

		win.poll()

		if win.quit():
			state = 'quit'

		key = win.key_press()
		if key == u'c':
			color_scheme = (color_scheme + 1) % len(color_schemes)
			print 'Using color scheme', color_scheme
			state = 'resize'
		elif key == u'e':
			limes_precision /= 1.1
			print 'limes precision:', limes_precision
			state = 'resize'
		elif key == u'E':
			limes_precision *= 1.1
			print 'limes precision:', limes_precision
			state = 'resize'
		elif key == u'n':
			N_min -= 1
			print 'N min:', N_min
			state = 'resize'
		elif key == u'N':
			N_min +=1
			print 'N min:', N_min
			state = 'resize'
		elif key == u'r':
			render_random = not render_random
			state = 'resize'
		elif key == u'a':
			(xmin, ymin) = (0.0, 0.0)
			(xmax, ymax) = (4.0, 4.0)
			state = 'resize'
		elif key == u'+':
			window_width *= 1.1
			state = 'resize'
		elif key == u'-':
			window_width /= 1.1
			state = 'resize'
		elif key == u'q':
			state = 'quit'
		elif key == u's':
			bmp = '/tmp/lyapunov-' + str( unixtime() ) + '.bmp'
			print 'Saving to', bmp, '...'
			win.saveBMP( bmp )
			print 'done.'

		mouse_button = win.mouse_press()
		if mouse_button == 1:
			(xmin,ymin) = win.mouse_coordinate()
			print 'New (xmin,ymin):', (xmin,ymin)
			
		elif mouse_button == 3:
			(xmax,ymax) = win.mouse_coordinate()
			print 'New (xmax,ymax):', (xmax,ymax)
			state = 'resize'

		mouse_pos = win.mouse_move()
		if mouse_pos:
			print >>sys.stderr, win.coordinate( mouse_pos )

		if state == 'rendering':
			win.update( 10.0 )
		else:
			win.update( 1.0 )

	sleep( 0.05 )

