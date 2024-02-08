class SearchProblem:
    def start_state(self):
        raise NotImplementedError()

    def actions(self, state):
        raise NotImplementedError()

    def cost(self, state, action):
        raise NotImplementedError()

    def succ(self, state, action):
        raise NotImplementedError()

    def is_end(self, state):
        raise NotImplementedError()


class GoatProblem(SearchProblem):
    class State:
        # s0 = State({'F', 'W', 'G', 'C'}, {})
        def __init__(self, left, right):
            self.left = left
            self.right = right

    def start_state(self):
        return self.State({'F', 'W', 'G', 'C'}, set())

    def cost(self, state, action):
        return 1

    def is_end(self, state):
        return state.left == set() and state.right == {'F', 'W', 'G', 'C'}

    # A = {'F', 'FW', 'FG', 'FC'}
    def succ(self, state, action):
        if 'F' in state.left:
            # set('FW') = {'F', 'W'}
            return self.State(state.left - set(action), state.right | set(action))
        else:
            return self.State(state.left | set(action), state.right - set(action))

    def actions(self, state):
        def no_eating(s):
            # returns True if nothing gets eaten in state s
            non_farmer_set = s.left if 'F' in s.right else s.right
            return not({'W', 'G'} <= non_farmer_set or {'G', 'C'} <= non_farmer_set)

        farmer_set = state.right if 'F' in state.right else state.left
        possible_actions = ['F'] + ['F' + x for x in farmer_set if x != 'F']
        return [a for a in possible_actions if no_eating(self.succ(state, a))]

