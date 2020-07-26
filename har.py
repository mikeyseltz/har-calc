
import numpy as np 
from math import tan, cos, acos, sin, degrees, radians

#inputs
msl_TOF = 40
start_alt = 30000
end_alt = 500 # or solve for this (i.e. radar horizon)
first_90_time = 10
first_90_dive = False
second_90_time = 6
second_90_dive = True
dive_angle = 50

#constants
g_onset = 3 # g's per second

#utilities
def level_turn_radius(velocity, bank): # bank in degrees, velocity in knots
	return velocity**2 / (11.26 * tan(radians(bank))) # returns radius in feet

def level_turn_rate(velocity, bank):
	return (1091 * tan(radians(bank)))/velocity # returns degrees per second
 
def level_turn_g(bank):
	return 1 / cos(radians(bank)) # returns g loading

def bank_for_g(g):
	return degrees(acos(1/g)) # returns degrees of bank in level turn at "g" loading

def g_performance(vel, g):
	bank = bank_for_g(g)
	rate = level_turn_rate(vel, bank)
	radius = level_turn_radius(vel, bank)
	return (rate, radius)

# phase 1: first 90
def first_90(vel, g, level=True): # returns (time, alt delta, range delta)
	if level:
		time = (90 / g_performance(vel, g)[0]) + (g/g_onset) # over simplified, need to integrate over time if want better acc.
		alt = 0
		rng = -g_performance(vel, g)[1] # no penalty for g onset...need calculus
		return {'time': time, 'alt': alt, 'rng': rng}
	else:
		pass


# phase 2:  second 90

# phase 3:  accel in dive

# phase 4:  straight line dive

# phase 5:  recover to level







#solve for time to established dive

#solve for radar horizon // or input this (altitude of terrain?)

#solve for time to below horizon

#solve for turn radius (in dive)
