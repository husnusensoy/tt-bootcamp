from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Run:
    milage: float
    duration: float
    location: Tuple[float, float]
    location_desc: str
    run_name: str = None

    def speed(self) -> float:
        return self.milage / self.duration

    def pace(self) -> float:
        return 1 / self.speed()

    def get_location_desc_by_location(self):
        return self.location_desc


def fn1(r: Run) -> float:
    return r.milage


def fn2(r: Run) -> float:
    return r.pace


def average(elements: list) -> float:
    n = len(elements)

    return sum(elements) / n


def top_loc_fn(t: Tuple[str, int]) -> int:
    loc, count = t

    return count


class RunApp:
    runs: List[Run]

    def __init__(self) -> None:
        self.runs = []

    def add_run(self, run: Run):
        self.runs.append(run)

    def best_pace(self) -> Run:
        return min(self.runs, key=lambda r: r.pace)

    def longest_run(self) -> Run:
        return max(self.runs, key=lambda r: r.milage)

    def top_loc(self) -> str:
        def top_loc_fn(t: Tuple[str, int]) -> int:
            loc, count = t

            return count

        aggr = {}

        for r in self.runs:
            aggr[r.location_desc] = aggr.get(r.location_desc, 0) + 1

        # {'Belgrad': 2, "MacFit":1}

        # run_count_by_loc.items() --> [('Belgrad', 2), ('MacFit',1)]

        loc, _ = max(((loc, cnt) for loc, cnt in aggr.items()), key=top_loc_fn)

        return loc

    def bottom_loc(self) -> str:
        aggr = {}

        for r in self.runs:
            aggr[r.location_desc] = aggr.get(r.location_desc, 0) + 1

        # {'Belgrad': 2, "MacFit":1}

        # run_count_by_loc.items() --> [('Belgrad', 2), ('MacFit',1)]

        loc, _ = min(((loc, cnt) for loc, cnt in aggr.items()), key=top_loc_fn)

        return loc

    def avg_milage_for_top_loc(self) -> float:
        run_made_in_top_location = [
            r.milage for r in self.runs if r.location_desc == self.top_loc()
        ]

        return average(run_made_in_top_location)

    def avg_milage_for_bottom_loc(self) -> float:
        run_made_in_top_location = [
            r.milage for r in self.runs if r.location_desc == self.bottom_loc()
        ]

        return average(run_made_in_top_location)

    def statistics(self):
        return self.avg_milage_for_top_loc() / self.avg_milage_for_bottom_loc()


milages = [4.38, 3.11, 4.82]
durations = [37.37, 33.47, 41.48]
locations = [(40.2, 36.3)] * 3
locations_desc = ["Belgrad", "MacFit", "Belgrad"]
runs_desc = ["Tuesday Run", "Treadmill Walk", "Before YKB Run"]


def test_my_best_pace_func():
    app = RunApp()

    for mile, dur, loc, loc_d, run_name in zip(
        milages, durations, locations, locations_desc, runs_desc
    ):
        r = Run(
            milage=mile,
            duration=dur,
            location=loc,
            location_desc=loc_d,
            run_name=run_name,
        )

        app.add_run(r)

    assert app.best_pace() == Run(
        4.38,
        37.37,
        location=(40.2, 36.3),
        location_desc="Belgrad",
        run_name="Tuesday Run",
    )


def test_my_longest_run_func():
    app = RunApp()

    for mile, dur, loc, loc_d, run_name in zip(
        milages, durations, locations, locations_desc, runs_desc
    ):
        r = Run(
            milage=mile,
            duration=dur,
            location=loc,
            location_desc=loc_d,
            run_name=run_name,
        )

        app.add_run(r)

    assert app.best_pace() == Run(
        milage=4.82,
        duration=41.48,
        location=(40.2, 36.3),
        location_desc="Belgrad",
        run_name="Before YKB Run",
    )
