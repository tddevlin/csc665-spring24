import math


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

        def __repr__(self):
            return f'{"".join(self.left):4} || {"".join(self.right):4}'

    def start_state(self):
        return self.State({'F', 'W', 'G', 'C'}, set())

    def cost(self, state, action):
        return 1

    def is_end(self, state: State):
        return state.left == set() and state.right == {'F', 'W', 'G', 'C'}

    # action is one of 'F', 'FW', 'FG', 'FC'
    def succ(self, state, action):
        if 'F' in state.left:
            # set('FW') == {'F', 'W'}
            return self.State(state.left - set(action), state.right | set(action))
        else:
            return self.State(state.left | set(action), state.right - set(action))

    def actions(self, state):
        def no_eating(s):
            # return True if nothing gets eaten in state s
            non_farmer_side = s.left if 'F' in s.right else s.right
            return not ({'W', 'G'} <= non_farmer_side or {'G', 'C'} <= non_farmer_side)

        farmer_side = state.right if 'F' in state.right else state.left
        possible_actions = ['F'] + ['F' + x for x in farmer_side if x != 'F']
        return [action for action in possible_actions if no_eating(self.succ(state, action))]


class BacktrackingSearch:
    def __init__(self, problem: SearchProblem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def recurse(self, state, path, cost):
        if self.problem.is_end(state):
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_path = path
            return

        for action in self.problem.actions(state):
            next_state = self.problem.succ(state, action)
            if next_state not in self.explored:
                self.explored.add(next_state)
                self.recurse(next_state, path + [path], cost + self.problem.cost(state, action))

    def solve(self):
        self.recurse(self.problem.start_state(), [], 0)


if __name__ == '__main__':
    gp = GoatProblem()
    backtracker = BacktrackingSearch(gp)
    backtracker.solve()  # this line throws a RecursionError... why?
