from math import tan, cos, acos, sin, degrees, radians
# constants


class Calculator:

    def __init__(self, g_onset):
        self.g_onset = g_onset

    # get radius in feet
    def level_turn_radius(self, velocity, bank):
        return velocity**2 / (11.26 * tan(radians(bank)))

    # get degrees per second
    def level_turn_rate(self, velocity, bank):
        return (1091 * tan(radians(bank)))/velocity

    # get g loading for level turn
    def level_turn_g(self, bank):
        return 1 / cos(radians(bank))

    # get bank based on g (level turn)
    def bank_for_g(self, g):
        return degrees(acos(1/g))

    def g_performance(self, vel, g):
        bank = self.bank_for_g(g)
        rate = self.level_turn_rate(vel, bank)
        radius = self.level_turn_radius(vel, bank)
        return (rate, radius)

    def time_to_act(self, time, vel):
        time = time  # how long it takes to react
        rng = -vel*1.8781*time
        return {'time': time, 'alt': 0, 'rng': rng}

    def first_90(self, vel, g, dive=0):
        # need better model for g onset
        time = (90 / self.g_performance(vel, g)[0]) + (g/self.g_onset)
        alt = 0
        rng = -self.g_performance(vel, g)[1]  # no penalty for g onset...
        return {'time': time, 'alt': alt, 'rng': rng}

    def second_90(self, vel, g, dive):
        time = 90 / self.g_performance(vel, g)[0]
        alt = sin(radians(dive))*self.g_performance(vel, g)[1]
        rng = cos(radians(dive))*self.g_performance(vel, g)[1]
        return {'time': time, 'alt': alt, 'rng': rng, 'dive': dive}

    def accel_in_dive(self, start_vel, end_vel, dive):
        # const accel rate of 50 knots per second
        accel_rate = 50
        time = (end_vel - start_vel) / accel_rate
        sin_dive = sin(radians(dive))
        cos_dive = cos(radians(dive))
        # get vertical descent rates in feet per second
        st_vert_rate = sin_dive*start_vel*1.68781  # knots to fps
        end_vert_rate = sin_dive*end_vel*1.68781
        # get horizontal travel rates in fps
        st_horiz_rate = cos_dive*start_vel*1.68781
        end_horiz_rate = cos_dive*end_vel*1.68781
        # calculate altitude lost during acceleration
        alt = (st_vert_rate * time) + \
              ((end_vert_rate * time)-(st_vert_rate*time))/2
        # calculate range delta during accel
        rng = (st_horiz_rate * time) + \
              ((end_horiz_rate * time)-(st_horiz_rate*time))/2
        return {'time': time, 'alt': alt, 'rng': rng, 'vel': end_vel}

    def straight_dive(self, vel, dive, st_alt):
        descent_rate = sin(radians(dive))*vel*1.68781
        alt_to_lose = st_alt - (dive/0.01)  # 1% dive angle
        time = alt_to_lose / descent_rate  # time in seconds until recov.
        rng = cos(radians(dive))*vel*1.68781*time
        return {'time': time, 'alt': alt_to_lose, 'rng': rng}

    def recover_to_level(self, vel, st_dive, st_alt):
        min_alt = 500  # break this hard code at some point
        alt = st_alt
        dive = st_dive
        time = 0
        rng = 0
        def des(x): return sin(radians(x))*vel*1.68781  # feet per second
        def rng_inc(x): return cos(radians(x))*vel*1.68781
        while alt > min_alt:
            dive = alt * 0.01
            alt -= des(dive)
            rng += rng_inc(dive)
            time += 1
        dive = 0
        return {'time': time, 'alt': st_alt - alt, 'rng': rng, 'dive': dive}
