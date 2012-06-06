#!/usr/bin/env python
# -*- coding: utf-8 -*-

# inspired by https://christopherolah.wordpress.com/2009/12/19/formation-of-escape-time-fractals/
# potentially approaching https://christopherolah.wordpress.com/2011/08/08/the-real-3d-mandelbrot-set/ ;)

from context import *
from time import time

class Julia ( Context ):

	def __init__ ( self ):

		vertex_shader = open( 'julia.vert', 'r' ).read()
		fragment_shader = open( 'julia.frag', 'r' ).read()

		# specify custom variables
		self.xmin, self.xmax = -2.0, 1.0	# complex coordinate system
		self.ymin, self.ymax = -1.5, 1.5
		 
		self.width = 523					# window size
		self.height = 523

		self.delay = 230.0
		
		self.iter = -1.0					# initial values
		self.auto = True
		self.t0 = time()

		super ( Julia, self ).__init__ ( "Juulia", self.width, self.height, 350, 50, 
											vertex_shader, fragment_shader )

		# clear color and depth buffer
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

		# specify callback functions
		glutIdleFunc( self.display )


	def display ( self ):

		if self.auto: self.iter += ( time() - self.t0 ) / self.delay

		# pass variables to shaders
		MyIter = glGetUniformLocation( self.shader, "MyIter" )
		glUniform1f( MyIter, self.iter )

		# glMatrixMode( GL_MODELVIEW )		# it's the default anyway
		# glLoadIdentity()

		# draw full-sized rectangle
	 	glBegin( GL_QUADS )
		glVertex2f( self.xmin, self.ymin )
		glVertex2f( self.xmin, self.ymax )
		glVertex2f( self.xmax, self.ymax )
		glVertex2f( self.xmax, self.ymin )
	 	glEnd()
	 	
	 	# glFlush()
	 	glutSwapBuffers()					# 


	def reshape ( self, width, height ):
		'''Adapt size of model relative to window size.'''

		glMatrixMode( GL_PROJECTION )
		glLoadIdentity()

		# project eye coordinates to clip coordinates ( complex plane to screen )
		glOrtho( self.xmin, self.xmax, self.ymin, self.ymax, -1.0, 1.0 )

		# transform normalized device coordinates to window coordinates
		glViewport( 0, 0, width, height )	# define viewport, here: ALL the window


	def keyboard ( self, *args ):

		# pass in ( key, x, y ) tuples
		if args[0] == '\x1b':				# exit on esc
			sys.exit()
		
		elif args[0] == 'c':
			self.auto = False if self.auto else True
			txt = "Auto-update." if self.auto else "Manual update. Press 'x' to step."
			print txt
		
		elif args[0] == 'x':
			self.iter += 1
			# print( "step " + str( self.iter ) )

		elif args[0] == '-':
			if self.iter >= 0.0: self.iter -= 1.0


if __name__ == '__main__':
	print "Press ESC to quit"
	print "press 'c' to switch between automatic and manual mode"
	print "Press 'x' to step thru iterations"
	print "Press '-' to return to previous iteration"
	Julia().run()