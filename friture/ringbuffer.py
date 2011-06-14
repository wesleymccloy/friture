#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timothée Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

from numpy import zeros

class RingBuffer():
	def __init__(self):
		# FIXME the buffer length could be made dynamic based on the needs
		self.buffer_length = 100000.
		self.buffer = zeros((1, 2*self.buffer_length))
		self.offset = 0

	def push(self, floatdata):
		# update the circular buffer
		
		dim = floatdata.shape[0]
		l = floatdata.shape[1]

		if dim <> self.buffer.shape[0]:
			# switched from single to dual channels or vice versa  
			self.buffer = zeros((dim, 2*self.buffer_length))
			self.offset = 0
		
		if l > self.buffer_length:
			raise StandardError("buffer error")
		
		# first copy, always complete
		self.buffer[:, self.offset : self.offset + l] = floatdata[:,:]
		# second copy, can be folded
		direct = min(l, self.buffer_length - self.offset)
		folded = l - direct
		self.buffer[:, self.offset + self.buffer_length: self.offset + self.buffer_length + direct] = floatdata[:, 0 : direct]
		self.buffer[:, :folded] = floatdata[:,direct:]
		
		self.offset = int((self.offset + l) % self.buffer_length)

	def data(self, length):
		start = self.offset + self.buffer_length - length
		stop = self.offset + self.buffer_length
		return self.buffer[:, start : stop]
