import random

class Statistic(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.timeline = Timeline()

    def shift_request(self, request, state):
        request.start = state.end + 1
        return request

    def create_new_state(self, request):
        new_state = State()
        new_state.start = request.start
        average = request.dest.average
        deviation = request.dest.deviation
        new_state.end = new_state.start + random.randint(average - deviation, average + deviation)
        new_state.node = request.dest
        return new_state

    def add_req(self, request):
        existing_state = self.timeline.state_for(request.dest, request.start)
        if existing_state:
            request = self.shift_request(request, existing_state)
            self.add_req(request)
        else:
            new_state = self.create_new_state(request)
            self.timeline.add_state(new_state)


    def to_report(self):
        # TODO
        pass


class Timeline:
    def __init__(self):
        self.time = []
        self.add_time()

    def state_for(self, dest, t):
        return self.time[t].get(dest)

    def add_time(self):
        self.time.extend([dict() for i in range(0, 101)])


    def add_state(self, state):
        for t in range(state.start, state.end + 1):
            dict = self.time[t]
            dict[state.node] = state


class State:
    def __int__(self):
        pass