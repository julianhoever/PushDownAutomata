class Cellar:
    def __init__(self, initial_cellar=None):
        self._elements = [] if initial_cellar is None else initial_cellar[::-1]

    def push(self, element):
        self._elements.append(element)

    def pop(self):
        return self._elements.pop() if len(self._elements) > 0 else None

    def to_list(self):
        return self._elements[::-1]


class DeterministicPushDownAutomata:
    def __init__(self, start_state, end_states, state_transitions, cellar_symbol):
        self._start_state = start_state
        self._end_states = end_states
        self._state_transitions = state_transitions
        self._cellar_symbol = cellar_symbol

        self._cellar = Cellar([self._cellar_symbol])
        self._current_state = self._start_state

    def accepts_word(self, word):
        word = list(word) + [None]
        new_state = self._start_state

        print("Current state:", self._current_state)
        print("Cellar", self._cellar.to_list())
        print("---")

        for char in word:
            state_combination = (self._current_state, char, self._cellar.pop())
            try:
                new_state, cellar_head = self._state_transitions[state_combination]
                self._current_state = new_state

                if cellar_head is not None:
                    for c in reversed(cellar_head):
                        self._cellar.push(c)

                print("Current state:", self._current_state)
                print("Cellar", self._cellar.to_list())
                print("---")

                if new_state in self._end_states:
                    return True

            except KeyError:
                return False

        return new_state in self._end_states


if __name__ == "__main__":
    automata = DeterministicPushDownAutomata(
        start_state="z0",
        end_states=["z2"],
        state_transitions={
            ("z0", "a", "#"): ("z0", "a#"),
            ("z0", "a", "a"): ("z0", "aa"),
            ("z0", "b", "a"): ("z1", None),
            ("z1", "b", "a"): ("z1", None),
            ("z1", None, "#"): ("z2", None)
        },
        cellar_symbol="#"
    )

    print(automata.accepts_word("aaabbb"))
