import random

class Statistic(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.timeline = Timeline()

    def add_req(self, request):
        existing_state = self.timeline.state_for(request.dest, request.start)
        if existing_state:
            request = self.shift_request(request, existing_state)
            self.add_req(request)
        else:
            new_state = self.create_new_state(request)
            self.timeline.add_state(new_state)


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


    def to_report(self):
        # TODO
        pass

    def get_node_stats(self, node):
        states = self.timeline.all_states_for(node)


class Timeline:
    def __init__(self):
        self.time = []
        self.add_time()

    def state_for(self, dest, t):
        return self.time[t].get(dest)

    def add_time(self):
        self.time.extend([dict() for i in range(101)])


    def add_state(self, state):
        for t in range(state.start, state.end + 1):
            dict = self.time[t]
            dict[state.node] = state

    def all_states_for(self, node=None, moment=None):
        time = [moment] if moment else range(len(self.time))

        states = []
        for t in time:
            state_dict = self.time[t]
            if state_dict:
                states_to_add = [state_dict.get(node)] if node else state_dict.values()
                states.extend([s for s in states_to_add if s not in states])

        return states


class State:
    def __init__(self, node=None, start=None, end=None):
        self.node = node
        self.start = start
        self.end = end