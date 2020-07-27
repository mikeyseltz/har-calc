
from math import tan, cos, acos, sin, degrees, radians
from utils import Calculator


class Engagement:

	state = {'alt': None, 'vel':None, 'rng':None, 'dive':0, 'alive':True, 'time':0}

	def __init__(self, missile=None):
		self.missile = missile

	def execute(self, st_alt=30000, st_vel=400, dive=45, first_90_dive=0, end_vel=500):
		c = Calculator(3) # 3 second g-onset hard coded for now
		self.state['alt'] = float(input("start altitude in feet >>> "))
		self.state['vel'] = float(input("start speed in knots >>> "))
		self.state['rng'] = float(input("starting range to tgt in nm >>> "))*6036
		dive = float(input("target dive angle >>> "))
		print(f"starting at {self.state['alt']}ft and {self.state['vel']} knots, diving to {dive} degrees")
		delay = float(input("how long to react in seconds >>> "))
		self.update_state(c.time_to_act(delay, self.state['vel']))

		g = float(input("how many gs will you pull? >>> "))
		self.update_state(c.first_90(self.state['vel'], g))
		self.update_state(c.second_90(self.state['vel'], dive))
		end_vel = int(input('what will you accelerate to in ktas? >>> '))
		self.update_state(c.accel_in_dive(self.state['vel'], end_vel, self.state['dive']))
		self.update_state(c.straight_dive(self.state['vel'], self.state['dive'],self.state['alt']))

	def update_state(self, deltas):
		starting = self.state
		self.state['alt'] = starting['alt'] - deltas['alt']
		self.state['rng'] = starting['rng'] + deltas['rng']
		self.state['time'] = starting['time'] + deltas['time']
		try:
			self.state['dive'] = deltas['dive'] 
		except:
			pass
		try:
			self.state['vel'] = deltas['vel']
		except:
			pass

		print(f"At time {self.state['time']}: {self.state['alt']}ft, Rng: {self.state['rng']/6036}nm, Dive: {self.state['dive']}deg")


#solve for time to established dive

#solve for radar horizon // or input this (altitude of terrain?)

#solve for time to below horizon

#solve for turn radius (in dive)
