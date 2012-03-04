import random

STAT_STRING = """
Node #{node_id}:
\tType:\t\t\t\t{type}
\tRequests sent:\t\t{req_sent}
\tRequests proceed:\t{req_proc}
\tUtilization:\t\t{util}
\tAvailability:\t\t{avail}
"""

class Statistic(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.requests = []
        self.timeline = Timeline()
        self.timeline.add_random_unavailabilities(nodes)

    def add_req(self, request):
        self.requests.append(request) if request not in self.requests else None

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
        average = self.nodes[request.dest].average
        deviation = self.nodes[request.dest].deviation
        new_state.end = new_state.start + random.randint(average - deviation, average + deviation)
        new_state.node = request.dest
        return new_state


    def to_report(self):
        return "\n".join(self.get_node_stats(node) for node in self.nodes)


    def get_node_stats(self, node):
        node_id = self.nodes.index(node)
        states = self.timeline.all_states_for(node_id)
        return self.fill_stat_string(node_id, states)

    def fill_stat_string(self, node_id, states):
        return STAT_STRING.format(
            node_id=node_id,
            type=self.nodes[node_id].__class__.__name__,
            req_sent=len([r for r in self.requests if r.src == node_id]),
            req_proc=len(states),
            util=(sum([s.end - s.start for s in states if not s.isUnavailable]) / float(len(self.timeline.time))),
            avail=(1 - sum([s.end - s.start for s in states if s.isUnavailable]) / float(len(self.timeline.time))))


class Timeline:
    def __init__(self):
        self.time = []
        self.add_time()

    def state_for(self, dest, t):
        return self.time[t].get(dest)

    def add_time(self):
        self.time.extend([dict() for i in range(100)])


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
                states_to_add = [state_dict.get(node)] if node is not None else state_dict.values()
                states.extend([s for s in states_to_add if s and s not in states])

        return states

    def add_random_unavailabilities(self, nodes):
        for i in range(len(nodes)):
            length = random.randint(0, 10)
            start = random.randint(0, len(self.time) - length)
            state = Unavailability(i, start, start + length)
            self.add_state(state)


class State:
    def __init__(self, node=None, start=None, end=None):
        self.node = node
        self.start = start
        self.end = end
        self.isUnavailable = False


class Unavailability(State):
    def __init__(self, node=None, start=None, end=None):
        self.node = node
        self.start = start
        self.end = end
        self.isUnavailable = True