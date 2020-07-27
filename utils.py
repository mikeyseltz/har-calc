from math import tan, cos, acos, sin, degrees, radians
#constants

class Calculator:

    def __init__(self, g_onset):
        self.g_onset = g_onset

    def level_turn_radius(self, velocity, bank): # bank in degrees, velocity in knots
        return velocity**2 / (11.26 * tan(radians(bank))) # returns radius in feet

    def level_turn_rate(self, velocity, bank):
        return (1091 * tan(radians(bank)))/velocity # returns degrees per second
     
    def level_turn_g(self, bank):
        return 1 / cos(radians(bank)) # returns g loading

    def bank_for_g(self, g):
        return degrees(acos(1/g)) # returns degrees of bank in level turn at "g" loading

    def g_performance(self, vel, g):
        bank = bank_for_g(g)
        rate = level_turn_rate(vel, bank)
        radius = level_turn_radius(vel, bank)
        return (rate, radius)

    def time_to_act(self, time, vel):
        time = time # how long it takes to react
        rng = -vel*1.8781*time
        return {'time': time, 'alt': 0, 'rng': rng}

    def first_90(self, vel, g, dive=0): # returns (time, alt delta, range delta)
        time = (90 / g_performance(vel, g)[0]) + (g/self.g_onset) # over simplified, need to integrate over time if want better acc.
        alt = 0
        rng = -g_performance(vel, g)[1] # no penalty for g onset...need calculus // range is negative, ie. closure
        return {'time': time, 'alt': alt, 'rng': rng}
        
    def second_90(self, vel, g, dive): # returns (time, alt delta, range delta)
        time = 90 / g_performance(vel, g)[0]
        alt = sin(radians(dive))*g_performance(vel, g)[1]
        rng = cos(radians(dive))*g_performance(vel, g)[1] # range is increasing now
        return {'time': time, 'alt': alt, 'rng': rng, 'dive':dive}

    def accel_in_dive(self, start_vel, end_vel, dive): # should we be using mach or TAS?
        accel_rate = 50 # const accel rate of 50 knots per second
        time = (end_vel - start_vel) / accel_rate
        sin_dive = sin(radians(dive))
        cos_dive = cos(radians(dive))
        # get vertical descent rates in feet per second
        st_vert_rate = sin_dive*start_vel*1.68781 # converts knots to fps
        end_vert_rate = sin_dive*end_vel*1.68781
        # get horizontal travel rates in fps
        st_horiz_rate = cos_dive*start_vel*1.68781
        end_horiz_rate = cos_dive*end_vel*1.68781
        # calculate altitude lost during acceleration
        alt = (st_vert_rate * time) + ((end_vert_rate * time)-(st_vert_rate*time))/2
        # calculate range delta during accel
        rng = (st_horiz_rate * time) + ((end_horiz_rate * time)-(st_horiz_rate*time))/2
        return {'time': time, 'alt': alt, 'rng': rng, 'vel': end_vel}

    def straight_dive(self, vel, dive, st_alt): # terminates at 4500' <-- hard coded for now
        descent_rate = sin(radians(dive))*vel*1.68781
        alt_to_lose = st_alt - 4500
        time = alt_to_lose / descent_rate # time in seconds until at 4500'
        rng = cos(radians(dive))*vel*1.68781*time
        return {'time': time, 'alt': alt_to_lose, 'rng': rng}
