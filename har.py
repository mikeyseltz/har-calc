
from math import tan, cos, acos, sin, degrees, radians
from utils import Calculator


def main():

	st_alt = float(input("start altitude in feet >>> "))
	st_vel = float(input("start speed in knots >>> "))
	st_rng = float(input("starting range to tgt in nm >>> "))*6036
	delay = float(input("how long to react in seconds >>> "))
	tgt_dive = float(input("target dive angle >>> "))
	g = float(input("how many gs will you pull? >>> "))
	end_vel = float(input('what will you accelerate to in ktas? >>> '))

	e = Engagement({'alt': st_alt, 'vel': st_vel, 'end_vel' : end_vel, 'rng': st_rng, 'dive': 0, 'g' : g, 'alive': True, 'time': 0, 'target_dive' : tgt_dive, 'delay' : delay})
	e.execute()

class Engagement:

	def __init__(self, state, missile=None):
		self.missile = missile
		self.state = state

	def execute(self):
		c = Calculator(3) # 3 second g-onset hard coded for now
		dive = self.state['target_dive']
		print(f"starting at {self.state['alt']}ft and {self.state['vel']} knots, diving to {dive} degrees")

		self.update_state(c.time_to_act(self.state['delay'], self.state['vel']))
		self.update_state(c.first_90(self.state['vel'], self.state['g']))
		self.update_state(c.second_90(self.state['vel'], self.state['g'], dive))
		self.update_state(c.accel_in_dive(self.state['vel'], self.state['end_vel'], self.state['dive']))
		self.update_state(c.straight_dive(self.state['vel'], self.state['dive'],self.state['alt']))
		self.update_state(c.recover_to_level(self.state['vel'], self.state['dive'], self.state['alt']))

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

		# self.check_for_death()

		print(f"At time {self.state['time']:.1f}: {self.state['alt']:.0f}ft, Rng: {(self.state['rng']/6036):.1f}nm, Dive: {self.state['dive']:.1f}deg")

	# def check_for_death(self):
	# 	if self.state['time'] > self.missile.tof:
	# 		pass
	# 	else:
	# 		pass

if __name__ == '__main__':
    main()

# solve for time to established dive

# solve for radar horizon // or input this (altitude of terrain?)

# solve for time to below horizon

# solve for turn radius (in dive)
