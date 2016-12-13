from __future__ import unicode_literals

from time import sleep


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
    WAIT_TIME = 10

    def __init__(self, id, top_floor, bottom_floor=1):
        self.id = id
        # floor status
        self.floor = bottom_floor
        self.direction = 'up'
        self.occupied = False
        self.stops = []
        self.open = False

        # history & maintenance
        self.trips = 0
        self.mileage = 0     # total # of floors passed

    @property
    def is_moving(self):
        return not self.open and len(self.stops) > 0

    @property
    def is_open(self):
        return self.open

    @property
    def is_occupied(self):
        return self.occupied

    @property
    def ascending(self):
        return self.direction == 'up'

    def open_door(self):
        if not self.open:
            sleep(self.WAIT_TIME)
            self.open = True

    def close_door(self):
        if self.open:
            sleep(self.WAIT_TIME)
            self.open = False

    def add_stop(self, floor):
        """Add the requested floor to the list of stops (if not already in the list)"""
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
        if self.floor in self.stops:
            self.stops.remove(self.floor)
            self.open_door()


    def move(self):
        self.close_door()
        if self.direction == 'up' and max(self.stops) < self.floor:
            self.direction = 'down'
        elif self.direction == 'down' and min(self.stops) > self.floor:
            self.direction = 'up'
        self.move_one()


