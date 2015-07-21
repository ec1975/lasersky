#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lasersky.py
#  by 220@WKH for Timberland / Ache Producciones
#
#  Copyright 2015 220 <220@WKH>
#
#  controls eight lasers connected to an 818 relay board from electronicaestudio.com
#  lasers are controlled by using the GPIO pins on a Raspberry Pi computer
#
#  requires pygame library
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

gpio=False
debug=True

if gpio:
	import RPi.GPIO as GPIO

import pygame
import random
import time

# operation parameters (seconds)
p_mute_time_min = 5
p_mute_time_max = 10

#lasers setup
laser_pins   = [11, 12, 13, 15, 16, 18, 22, 7]
laser_values = [False, False, False, False, False, False, False, False]


#patterns
global pattern

global pattern_lapse
global pattern_time

global pattern_counter
global pattern_limit


# audio tracks list
atmosphere_tracks = ["mute", 
"atmosphere-digitaldrone-3L.wav",
"atmosphere-digitaldrone-5.wav",
"atmosphere-orbit-5.wav",
"atmosphere-spacedout-3L.wav",
"atmosphere-spacedout-5.wav",
"atmosphere-stonehench-3L.wav",
"atmosphere-stonehench-5.wav",
"atmosphere-digitaldrone-A-2L.wav",
"atmosphere-orbit-A-2L.wav",
"atmosphere-orbit-A-5.wav",
"atmosphere-orbit-E-3.wav",
"atmosphere-spacedout-A-2L.wav",
"atmosphere-spacedout-A-5.wav",
"atmosphere-spacedout-E-3.wav",
"atmosphere-stonehench-A-5.wav",
"atmosphere-stonehench-E-3.wav"
]

starscape_tracks = ["mute", 
"starscape-pulsar1-1in6-10.wav",
"starscape-pulsar1-4in8-6.wav",
"starscape-pulsar1-pebbles-6.wav",
"starscape-pulsar2-1in6-10.wav",
"starscape-pulsar2-4in6-10.wav",
"starscape-pulsar2-4in8-6.wav",
"starscape-pulsar2-pebbles-6.wav",
"starscape-strummer-1in6-10.wav",
"starscape-strummer-4in6-10.wav",
"starscape-strummer-4in8-6.wav",
"starscape-strummer-pebbles-6.wav",
"starscape-pulsar1-6.wav",
"starscape-pulsar2-1in6-E.wav",
"starscape-pulsar2-6.wav",
"starscape-strummer-1in6-E.wav",
"starscape-strummer-6.wav"
]

laser_tracks = [
"laser-backmasker.wav",
"laser-easternstar.wav",
"laser-nassalite.wav",
"laser-polarislead.wav",
"laser-spectralcloud.wav"
]


fx_tracks = [
"mute",
"fx-warper.wav",
"tech-bleep1.wav",
"tech-galactica.wav",
"tech-hijackL.wav",
"tech-hijack.wav",
"tech-opiumlong.wav",
"tech-opium.wav"
]

# storage
global atmos_channel
global atmos_lapse
global atmos_time
global atmos_running

global stars_channel
global stars_lapse
global stars_time

global fx_channel
global fx_lapse
global fx_time
global fx_running

global laser_sound
global laser_channel

### basic resources handling
def setNewAtmosphere (sound_channel):
	if debug:
		print ("setting new atmosphere!")
	next_filename = random.choice (atmosphere_tracks)
	
	if debug:
		print (next_filename)

	if next_filename=="mute":
		atmos_time = random.randint (p_mute_time_min, p_mute_time_max)
	else:
		atmos_sound = pygame.mixer.Sound (next_filename)
		sound_channel.play (atmos_sound)
		
		atmos_time = atmos_sound.get_length ()
	
	return atmos_time
	
def setNewLaser ():
	if debug:
		print ("setting new laser sound!")
	
	next_filename = random.choice (laser_tracks)
	
	if debug:
		print (next_filename)
	
	######################
	global laser_sound
	laser_sound = pygame.mixer.Sound (next_filename)
	
	return 0

	
def setNewStarscape (sound_channel):
	if debug:
		print ("setting new starscape!")
	next_filename = random.choice (starscape_tracks)
	if debug:
		print (next_filename)

	if next_filename=="mute":
		stars_time = random.randint (p_mute_time_min, p_mute_time_max)
	else:
		stars_sound = pygame.mixer.Sound (next_filename)
		sound_channel.play (stars_sound)
		
		stars_time = stars_sound.get_length ()
	
	return stars_time

def setNewFx (sound_channel):
	if debug:
		print ("setting new fx!")
	next_filename = random.choice (fx_tracks)
	if debug:
		print (next_filename)

	if next_filename=="mute":
		fx_time = random.randint (p_mute_time_min, p_mute_time_max)
	else:
		fx_sound = pygame.mixer.Sound (next_filename)
		#################
		sound_channel.play (fx_sound)
		
		fx_time = fx_sound.get_length ()
	
	return fx_time


### pattern management
def patternStep (pattern, pattern_counter):
	if pattern == 0:
		pattern_random ()
	if pattern == 1:
		pattern_fade_in (pattern_counter)
	if pattern == 2:
		pattern_fade_out (pattern_counter)
	if pattern == 3:
		pattern_quaternary (pattern_counter)
	if pattern == 4:
		pattern_quaternary (pattern_counter)
	if pattern == 5:
		pattern_evens (pattern_counter)
	if pattern == 6:
		pattern_odds (pattern_counter)
	if pattern == 7:
		pattern_full_on (pattern_counter)
	if pattern == 8:
		pattern_flicker (pattern_counter)
	return 0
	
def pattern_random ():
	if debug:
		print ("executing random pattern")
	for pin in laser_pins:
		v = random.randrange (2)
		laser_channel.play (laser_sound)
		if debug:
			print (v)
		
		if gpio:
			GPIO.output (pin, v)
			time.sleep (0.3)
	return 0
	
def pattern_flicker (pattern_counter):
	if debug:
		print ("executing random pattern")
	laser_channel.play (laser_sound)
	pin = random.choice (laser_pins)
	for i in range (10):
		if debug:
			print (pin)
		
		if gpio:
			GPIO.output (pin, 1)
			time.sleep (0.1)
			GPIO.output (pin, 0)
			time.sleep (0.1)
		
	for pin in laser_pins:
		v = random.randrange (2)
		laser_channel.play (laser_sound)
		if debug:
			print (v)
		
		if gpio:
			GPIO.output (pin, v)
			time.sleep (0.3)
	return 0

def pattern_fade_in (pattern_counter):
	if pattern_counter<1:
		if debug:
			print ("executing fade_in pattern")
		for pin in laser_pins:
			if gpio:
				GPIO.output (pin, False)
			if debug:
				print ("reset to off")
			

	else:
		if debug:
			print ("X: ")
			print (pattern_counter)
		pin = laser_pins [pattern_counter-1]
		if gpio:
			GPIO.output (pin, True)
		if debug:
			print ("turning pin on: ")
			print (pin)
		laser_channel.play (laser_sound)
		
	return 0

def pattern_fade_out (pattern_counter):
	if pattern_counter<1:
		if debug:
			print ("executing fade_out pattern")
		for pin in laser_pins:
			if gpio:
				GPIO.output (pin, True)
			if debug:
				print ("reset to on")

	else:
		if debug:
			print ("Y: ")
			print (pattern_counter)
		pin = laser_pins [pattern_counter-1]
		if gpio:
			GPIO.output (pin, False)
		if debug:
			print ("turning pin off: ")
			print (pin)
		laser_channel.play (laser_sound)
		
	return 0

def pattern_binary (pattern_counter):
	for pin in laser_pins:
		if gpio:
			GPIO.output (pin, False)
			time.sleep (0.25)
		if debug:
			print ("turn off")	
	
	a = random.randrange (8)
	b = a
	while b==a:
		b = random.randrange (8)
	
	if debug:
		print ("binary:")
		print (a)
		print (b)
	if gpio:
		GPIO.output (laser_pins [a], True)
		time.sleep (0.2)
		GPIO.output (laser_pins [b], True)
	laser_channel.play (laser_sound)
		
	return 0
	
def pattern_quaternary (pattern_counter):
	for pin in laser_pins:
		if gpio:
			GPIO.output (pin, False)
			time.sleep (0.25)
		if debug:	
			print ("turn off")	
	
	a = random.randrange (8)
	b = random.randrange (8)
	c = random.randrange (8)
	d = random.randrange (8)

	if debug:
		print ("quaternary:")
		print (a)
		print (b)
		print (c)
		print (d)
	
	if gpio:
		GPIO.output (laser_pins [a], True)
		laser_channel.play (laser_sound)
		time.sleep (0.2)
		GPIO.output (laser_pins [b], True)
		laser_channel.play (laser_sound)
		time.sleep (0.2)
		GPIO.output (laser_pins [c], True)
		laser_channel.play (laser_sound)
		time.sleep (0.2)
		GPIO.output (laser_pins [d], True)
		laser_channel.play (laser_sound)
	return 0

def pattern_full_on (pattern_counter):
	for pin in laser_pins:
		if gpio:
			GPIO.output (pin, False)
			time.sleep (0.25)
		laser_channel.play (laser_sound)
	return 0

def pattern_light_up (pattern_counter):
	if pattern_counter<1:
		if debug:
			print ("executing light_up pattern")
		for pin in laser_pins:
			if gpio:
				GPIO.output (pin, False)
			if debug:
				print ("reset to off")
	else:
		if debug:
			print ("Z: ")
			print (pattern_counter)
		pin = laser_pins [pattern_counter-1]
		if gpio:
			GPIO.output (pin, True)
		if debug:
			print ("turning pin on: ")
			print (pin)
		laser_channel.play (laser_sound)
	
	return 0
	
def pattern_evens (pattern_counter):
	a = 0
	
	while a<8:
		pin = laser_pins [a]
		if gpio:
			GPIO.output (pin, True)
		if debug:
			print (pin)
		laser_channel.play (laser_sound)
		
		a+= 2
	
	return 0
	
def pattern_odds (pattern_counter):
	a = 1
	
	while a<9:
		pin = laser_pins [a]
		if gpio:
			GPIO.output (pin, True)
		if debug:
			print (pin)
		laser_channel.play (laser_sound)
		
		a+= 2
	
	return 0
	

def main():
	print ("lasersky 1.0")
	print ("by 220 @ WKH")
	
	if gpio:
		GPIO.setmode (GPIO.BOARD)
		for pin in laser_pins:
			GPIO.setup (pin, GPIO.OUT)
	
	#4096
	pygame.mixer.init (frequency=44100, size=-16, channels=2, buffer=2048)
	pygame.mixer.set_num_channels (4)
	
	atmos_channel = pygame.mixer.Channel (0)
	stars_channel = pygame.mixer.Channel (1)
	fx_channel = pygame.mixer.Channel (2)
	global laser_channel
	laser_channel = pygame.mixer.Channel (3)
	
	atmos_channel.set_volume (1.0)
	stars_channel.set_volume (1.0)
	fx_channel.set_volume (0.75)
	laser_channel.set_volume (0.15)
	
	
	setNewLaser ()

	atmos_lapse = 0
	atmos_time = 0
	atmos_running = 0
	
	stars_lapse = 0
	stars_time = 0
	stars_running = 0
	
	fx_running = 0
	
	pattern_lapse = 0
	pattern_time = 3
	
	pattern_counter = 0
	pattern_change = True
	
	while True:
		# PATTERNS
		# change pattern
		if pattern_change==True:
			pattern_counter = 0
			pattern_change = False
			pattern = random.randrange (9)
			
			if pattern==0:
				pattern_limit = random.randrange (8, 10)
			if pattern==1:
				pattern_limit = 8
			if pattern==2:
				pattern_limit = 8
			if pattern==3:
				pattern_limit = random.randrange (6, 10)
			if pattern==4:
				pattern_limit = random.randrange (6, 10)
			if pattern==5:
				pattern_limit = random.randrange (4, 12)
			if pattern==6:
				pattern_limit = random.randrange (4, 12)
			if pattern==7:
				pattern_limit = random.randrange (6, 10)
			if pattern==8:
				pattern_limit = random.randrange (2, 4)
				
			setNewLaser ()
			pattern_time = random.randrange (1, 3)	
			
			if debug:
				print ("new pattern limit")
				print (pattern_limit)
				print ("new pattern time")
				print (pattern_time)
			
		
		if time.time()-pattern_lapse>pattern_time:
			s = patternStep (pattern, pattern_counter)
			pattern_counter = pattern_counter+1
			if pattern_counter>pattern_limit:
				pattern_change = True
			
			pattern_lapse = time.time ()


		# AUDIO
		# atmosphere
		if atmos_running==0:
			atmos_time = setNewAtmosphere (atmos_channel)
			
			atmos_lapse = time.time ()
			atmos_running = 1
			
			if debug:
				print ("new atmos_time")
				print (atmos_time)
			
		else:
			if time.time()-atmos_lapse>atmos_time:
				if atmos_channel.get_busy ()==0:
					atmos_running = 0
		
		# starscape			
		if stars_running==0:
			stars_time = setNewStarscape (stars_channel)
			
			stars_lapse = time.time ()
			stars_running = 1
			
			if debug:
				print ("new stars_time")
				print (stars_time)
			
		else:
			if time.time()-stars_lapse>stars_time:
				if stars_channel.get_busy ()==0:
					stars_running = 0

		# fx
		if fx_running==0:
			fx_time = setNewFx (fx_channel)
			
			fx_lapse = time.time ()
			fx_running = 1
			
			if debug:
				print ("new fx_time")
				print (fx_time)
			
		else:
			if time.time()-fx_lapse>fx_time:
				if fx_channel.get_busy ()==0:
					fx_running = 0


	return 0

if __name__ == '__main__':
	main()
