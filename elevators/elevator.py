from __future__ import unicode_literals

"""
Elevator features:
1. Initialize the elevator simulation with the desired number of elevators, and the desired number of floors.
Assume ground/min of 1.
2. Each elevator will report as is moves from floor to floor.
3. Each elevator will report when it opens or closes its doors.
4. An elevator cannot proceed above the top floor.
5. An elevator cannot proceed below the ground floor (assume 1 as the min).
6. An elevator request can be made at any floor, to go to any other floor.
7. When an elevator request is made, the unoccupied elevator closest to it will answer the call,
    unless an occupied elevator is moving and will pass that floor on its way.
    The exception is that if an unoccupied elevator is already stopped at that floor,
    then it will always have the highest priority answering that call.
8. The elevator should keep track of how many trips it has made, and how many floors it has passed.
    The elevator should go into maintenance mode after 100 trips, and stop functioning until serviced,
    therefore not be available for elevator calls.

"""


class Elevator(object):
    """Tracks the state of the elevator, assumes the actual physical elevator interacts with this class"""
    def __init__(self, id, top_floor, bottom_floor=1):
        self.id = id
        # floor status
        self.min_floor = bottom_floor
        self.max_floor = top_floor
        self.floor = bottom_floor
        self.direction = 'up'
        self.occupied = False
        self.stops = []
        self.open = True

        # history & maintenance
        self.trips = 0
        self.mileage = 0        # total number of floors passed since last maintanence
        self.total_mileage = 0  # lifetime total number of floors passed

    def __str__(self):
        if self.open:
            return 'Elevator {0} open on Floor {1}'.format(self.id, self.floor)
        elif self.stops:
            return 'Elevator {0} moving {2} passing Flo0r {1}'.format(self.id, self.floor, self.direction)
        else:
            return 'Elevator {0} waiting on Floor {1}'.format(self.id, self.floor)

    @property
    def is_moving(self):
        return not self.open and len(self.stops) > 0

    @property
    def is_open(self):
        return self.open

    @property
    def needs_maintanence(self):
        return not self.occupied and self.trips >= 100

    @property
    def is_occupied(self):
        return self.occupied

    @property
    def ascending(self):
        return self.direction == 'up'

    def can_access(self, floor):
        return self.min_floor <= floor <= self.max_floor and not self.needs_maintanence

    def moving_toward(self, floor):
        if not self.occupied:
            return False
        return (self.direction == 'up' and self.floor < floor) or (self.direction == 'down' and self.floor > floor)

    def distance_from(self, floor):
        return abs(self.floor - floor)

    def open_door(self):
        if not self.open:
            self.open = True

    def close_door(self):
        if self.open:
            # TODO stuff woud go here to avoid closing the door too quickly and wait if the door is blocked
            self.open = False

    def add_stop(self, floor):
        """Add the requested floor to the list of stops (if not already in the list)."""
        if floor < self.min_floor or floor > self.max_floor:
            raise ValueError("Cannot reach floor {}".format(floor))
        if floor != self.floor and floor not in self.stops:
            self.stops.append(floor)

    def passenger_request(self, floor):
        """passenger in the car pushed a floor button"""
        self.occupied = True
        self.add_stop(floor)
        self.move()

    def call_request(self, floor):
        """The call button on level 'floor' was pressed"""
        self.add_stop(floor)
        self.move()

    def move_one(self):
        self.floor += 1 if self.ascending else -1
        self.mileage += 1
        self.total_mileage += 1
        if self.floor in self.stops:
            self.stops.remove(self.floor)
            self.open_door()
            if not self.stops:
                self.occupied = False
                self.trips += 1
                self.direction = 'down' if self.ascending else 'up'

    def move(self):
        self.close_door()
        if self.direction == 'up' and max(self.stops) < self.floor:
            self.direction = 'down'
        elif self.direction == 'down' and min(self.stops) > self.floor:
            self.direction = 'up'
        self.move_one()

    def maintenance_completed(self):
        self.trips = 0
        self.mileage = 0


class Controller(object):
    def __init__(self, elevators, top_floor):
        self.elevators = [Elevator(i, top_floor) for i in range(elevators)]

    def call_light(self, floor):
        while True:
            available = [e for e in self.elevators if e.can_access(floor)]
            # see if an empty elevator is already there
            at_floor = [e for e in available if e.floor == floor and not e.is_occupied]
            if at_floor:
                at_floor[0].call_request(floor)
                break
            # if not find closest moving toward floor
            moving_to = [e for e in available if e.moving_toward(floor)].sort(lambda e: distance_from(floor))
            if moving_to:
                moving_to[0].call_request(floor)
                break
            # if none, find closest
            # otherwise all are occupied and moving away from floor pick one that will be empty soonest
            pass

