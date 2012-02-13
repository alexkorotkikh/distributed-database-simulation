import random

class Statistic(object):
    """docstring for Statistic"""

    def __init__(self, nodes):
        self.nodes = nodes
        self.timeline = Timeline()

    def add_req(self, request):
        state = self.timeline.state_for(request.dest, request.start)
        if state:
            request.start = state.end + 1
            self.add_req(request)
        else:
            state = State()
            state.start = request.start

            average = request.dest.average
            deviation = request.dest.deviation
            state.end = state.start + random.randint(average - deviation, average + deviation)

            state.node = request.dest
            self.timeline.add_state(state)

        pass

    def to_report(self):
        # TODO
        pass


class Timeline:
    def __init__(self):
        self.time = []
        self.add_time()

    def state_for(self, dest, t):
        return self.time[t].dest

    def add_time(self):
        self.time.extend([{}] * 100)

    def add_state(self, state):
        for t in range(state.start, state.end):
            self.time[t][state.dest] = state


class State:
    def __int__(self):
        pass