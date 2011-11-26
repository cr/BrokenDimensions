#!/usr/bin/env python

import pygame
import random
from time import time as unixtime

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
		self.surface = pygame.display.set_mode( (self.width, self.height) )
		self.surface.fill( (0, 0, 0) )
		self.update_time = unixtime()-100.0
		self.update()

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
		event = pygame.event.poll()
		return event.type == pygame.QUIT

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

