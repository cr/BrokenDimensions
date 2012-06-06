#!/usr/bin/env python
# -*- coding: utf-8 -*-

# adapted from http://www.seethroughskin.com/blog/?p=771
# which modified http://www.pygame.org/wiki/GLSLExample

# import OpenGL 
# OpenGL.ERROR_ON_COPY = True 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL import shaders

import time, sys

class Context( object ):
	'''Context with GLUT window'''

	def __init__ ( self, title="title", width=640, height=480, pos_x=50, pos_y=50, 
					vertex_shader=None, fragment_shader=None ):
	 
		# initialize GLUT library ( cf. window handling, user interactions )
		glutInit( sys.argv )
		glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
		# glutFullScreen()

		# initialize and create window
		glutInitWindowPosition( pos_x, pos_y ) 	# set upper left corner on screen
		glutInitWindowSize( width, height )
		self.window = glutCreateWindow( title )

		# register callback functions
		glutDisplayFunc( self.display )
		# glutIdleFunc( self.display )
		glutReshapeFunc( self.reshape )		# called on window creation as well
		glutKeyboardFunc( self.keyboard )
		glutMouseFunc( self.mouse )

		# specify clear values for some buffers and the shading technique to use
		# ( noted for explicity only, values are the defaults )
		glClearColor( 0.0, 0.0, 0.0, 0.0 )	# range [0;1]
		glClearDepth( 1.0 )					# range [0;1]
		glShadeModel( GL_SMOOTH )			# GL_FLAT or GL_SMOOTH

		# compile shaders
		if vertex_shader and fragment_shader:
			self.shader = shaders.compileProgram ( # uses OpenGL.GL.shaders
							shaders.compileShader( vertex_shader, GL_VERTEX_SHADER ),
							shaders.compileShader( fragment_shader, GL_FRAGMENT_SHADER ) )
			glUseProgram( self.shader )
		
		# print( glGetString( GL_VERSION ))
	
	
	def reshape ( self, width, height ):
		'''For subclass to implement callback for window resize events.'''
		# raise NotImplementedError

	def display ( self ):
		'''For subclass to implement their rendering behavior.'''
		raise NotImplementedError
	

	def keyboard ( self, *args ):
		# pass in ( key, x, y ) tuples
		'''For subclass to implement their keyboard behavior.'''
		# raise NotImplementedError


	def mouse ( *args ):
		'''For subclass to implement their mouse behavior.'''
		# raise NotImplementedError


	@staticmethod
	def run ():
		glutMainLoop()		# start event processing engine