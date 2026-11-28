#!/usr/bin/env python3
"""Finite checks of selected mathematical claims in chapters 3–5, 34 and 37.

These computations supplement the proofs in the text. They verify only the
finite instances described below, not the corresponding general theorems.
"""

from itertools import product
from fractions import Fraction
import cmath
import json


def has_infinite_path(x, transition, actions, safe, visited):
    """An infinite path in a finite graph exists iff a reachable cycle exists."""
    if x not in safe:
        return False
    if x in visited:
        return True
    return any(
        has_infinite_path(transition[x][a], transition, actions, safe, visited | {x})
        for a in actions[x]
    )


def main():
    states = range(3)
    actions = range(2)
    subsets = [
        {a for a, included in zip(actions, mask) if included}
        for mask in product([0, 1], repeat=2)
    ]
    observation_cases = 0
    for observation in product(range(2), repeat=3):
        readings = sorted(set(observation))
        for acceptable in product(subsets, repeat=3):
            exists = any(
                all(
                    dict(zip(readings, policy))[observation[x]] in acceptable[x]
                    for x in states
                )
                for policy in product(actions, repeat=len(readings))
            )
            intersection_condition = all(
                set.intersection(
                    *(acceptable[x] for x in states if observation[x] == reading)
                )
                for reading in readings
            )
            assert exists == bool(intersection_condition)
            observation_cases += 1

    closure_cases = 0
    for transition in product(states, repeat=3):
        for observation in product(range(2), repeat=3):
            readings = sorted(set(observation))
            exists = any(
                all(
                    observation[transition[x]]
                    == dict(zip(readings, coarse_rule))[observation[x]]
                    for x in states
                )
                for coarse_rule in product(readings, repeat=len(readings))
            )
            closure_condition = all(
                observation[x] != observation[z]
                or observation[transition[x]] == observation[transition[z]]
                for x in states
                for z in states
            )
            assert exists == closure_condition
            closure_cases += 1

    viability_cases = 0
    for size, vary_available_actions in [(2, True), (3, False)]:
        graph_states = range(size)
        action_sets = (
            list(product(subsets, repeat=size))
            if vary_available_actions
            else [tuple({0, 1} for _ in graph_states)]
        )
        for flat_transition in product(graph_states, repeat=2 * size):
            transition = [flat_transition[2 * x:2 * x + 2] for x in graph_states]
            for available in action_sets:
                for mask in product([0, 1], repeat=size):
                    safe = {x for x, included in zip(graph_states, mask) if included}
                    kernel = safe.copy()
                    while True:
                        reduced = {
                            x for x in kernel
                            if any(transition[x][a] in kernel for a in available[x])
                        }
                        if reduced == kernel:
                            break
                        kernel = reduced
                    cycle_reachable = {
                        x for x in graph_states
                        if has_infinite_path(x, transition, available, safe, set())
                    }
                    assert kernel == cycle_reachable
                    viability_cases += 1

    for numerator in range(-10, 61):
        gain = numerator / 20
        roots = (
            (1 + cmath.sqrt(1 - 4 * gain)) / 2,
            (1 - cmath.sqrt(1 - 4 * gain)) / 2,
        )
        stable = max(abs(root) for root in roots) < 1 - 1e-9
        assert stable == (0 < gain < 1)

    def performative_risk(parameter):
        return (1 - parameter / 2) ** 2 + parameter ** 2

    assert performative_risk(Fraction(2)) == 4
    assert performative_risk(Fraction(2, 5)) == Fraction(4, 5)
    assert 10 + 100 * .15 + .01 * 500 + 5 == 35
    assert 10 + 100 * .8 + .03 * 1000 + 5 == 125
    assert Fraction(120) * Fraction(2, 5) == 48
    print(json.dumps({
        "observation_cases": observation_cases,
        "closure_cases": closure_cases,
        "viability_cases": viability_cases,
        "delayed_control_parameter_points": 71,
        "numeric_examples": "passed",
        "scope": "Finite instance checks; the general proofs are in the manuscript."
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
