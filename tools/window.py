#!/usr/bin/env python

import pygame
import random
from time import time as unixtime
import struct

class Window( object ):

	def __init__( self, width, aspect=1.0, (xmin,ymin)=(0.,0.), (xmax,ymax)=(1.,1.) ):
		"""Create window object defined by pixel width, aspect ratio.
		You can specify a 2D interval as underlying math coordinate set.
		"""
		self.aspect = float( aspect )
		self.width = int( width )
		self.height = int( width / aspect )
		self.xmin = float( xmin )
		self.xmax = float( xmax )
		self.ymin = float( ymin )
		if ymin == ymax:
			self.ymax = float( ymin + (xmax-xmin) / aspect )
		else:
			self.ymax = float( ymax )
		self.xstep = float( (self.xmax-self.xmin)/self.width )
		self.ystep = float( (self.ymax-self.ymin)/self.height )

		pygame.init()
		self.surface = pygame.display.set_mode( (self.width, self.height), pygame.constants.RESIZABLE )
		self.surface.fill( (0, 0, 0) )
		self.update_time = unixtime()-100.0
		self.update()

		self.button_status = ( False, False, False )
		self.event = pygame.event.poll()

	def set_title( self, title ):
		pygame.display.set_caption( title )

	def plot( self, pixel, rgb = (1.0, 1.0, 1.0) ):
		self.surface.set_at( pixel, rgb )

	def update( self, frequency=4.0 ):
		if unixtime() - self.update_time > 1./frequency:
			self.surface.unlock()
			pygame.display.flip()
			self.update_time = unixtime()

	def coordinate( self, pixel ):
		"""Returns math coordinates for given pixel coordinates"""
		return ( pixel[0]*self.xstep + self.xmin, pixel[1]*self.ystep + self.ymin )

	def pixel( self, coord ):
		"""Returns pixel coordinates for given math coordinates"""
		return ( int( (coord[0]-self.xmin)/self.xstep ), int( (coord[1]-self.ymin)/self.ystep ) )

	def quit( self ):
		return self.event.type == pygame.QUIT

	def __iter__( self ):
		my = self.ymin
		for py in xrange( 0, self.height ):
			mx = self.xmin
			for px in xrange( 0, self.width ):
				yield ( (px,py), (mx,my) )
				mx += self.xstep
			my += self.ystep
		raise StopIteration

	def random( self ):
		arr = [ x for x in self ]
		while arr:
			pos = int( random.random() * len( arr ) )
			yield arr.pop( pos )

	def invert( self, (xmin,ymin), (xmax,ymax) ):
		self.surface.lock()

		for x in xrange(xmin,xmax):
			for y in xrange(ymin,ymax):
				c = self.surface.get_at((x,y))
				self.surface.set_at((x,y),(255-c[0],255-c[1],255-c[2],c[3]))

		self.surface.unlock()

	def saveBMP( self, name = '/tmp/window.bmp' ):
		width = self.surface.get_width()
		height = self.surface.get_height()

		# fix size to be multiple of 4 ; BMP doesn't like it any other way
		width -= width%4
		height -= height%4

		file = open( name, 'wb' )
		file.write( 'BM' + struct.pack( '<QIIHHHH', width*height*3+26,26, 12, width, height, 1,24) )
		self.surface.lock()

		for y in xrange( height-1, -1, -1 ):
			for x in xrange( width ):
				v = self.surface.get_at( (x, y) )
				file.write( struct.pack( 'BBB', v[2], v[1], v[0] ) )

		self.surface.unlock()
		file.close()

	def poll( self ):
		self.event = pygame.event.poll()
		if self.event.type == pygame.NOEVENT:
			return False
		else:
			return self.event.type

	def key_press( self ):
		if self.event.type == pygame.KEYDOWN:
			return self.event.unicode
		else:
			return False

	def mouse_press( self ):
		if self.event.type == pygame.MOUSEBUTTONDOWN:
			return self.event.button
		else:
			return False

	def mouse_move( self ):
		if self.event.type == pygame.MOUSEMOTION:
			return self.event.pos
		else:
			return False

	def mouse_position( self ):
		return pygame.mouse.get_pos()

	def mouse_coordinate( self ):
		return self.coordinate( self.mouse_position() )

