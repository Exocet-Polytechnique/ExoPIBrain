"""
This class will be used to determine whether the current electrical output of the fuel cells is
within the efficiency range. The csv file used can be found in data/eff_curves.csv
"""
import csv


class SystemEfficiency:
    def __init__(self, csv_data_path, threshold=0.05):
        """
        Initialize the class by pre-computing the optimal ranges based on the threshold
        """
        self.threshold = threshold

        with open(csv_data_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if row[0] == "e_load":
                    self.load_data = [float(v) for v in row[1:]]
                elif row[0] == "fc_efficiency":
                    self.efficiency_data = [float(v) for v in row[1:]]

        # we can compute this once at the start so we only need to compare the value to ranges
        # aftewards
        (
            self._perfect_range,
            self._good_range,
            self._optimal_load,
        ) = self._compute_optimal_ranges()

    def _compute_optimal_ranges(self):
        max_index, max_efficiency = max(
            enumerate(self.efficiency_data), key=lambda x: x[1]
        )
        min_perfect_eff = (1 - self.threshold) * max_efficiency
        min_good_eff = (1 - 5 * self.threshold) * max_efficiency

        def get_linear_approx(start_index, end_index, efficiency):
            # create a function of the form y = mx + b by computing the values of m and b
            delta_y = self.load_data[end_index] - self.load_data[start_index]
            delta_x = (
                self.efficiency_data[end_index] - self.efficiency_data[start_index]
            )
            m = delta_y / delta_x
            b = self.load_data[start_index] - m * self.efficiency_data[start_index]

            # then approximate the value using that function
            return m * efficiency + b

        def get_first_load_pt(efficiency):
            start = 0
            end = max_index
            for i in range(1, max_index):
                if self.efficiency_data[i] >= efficiency:
                    end = i
                    break
                start += 1

            # if the point comes before the value at index 0, it will be able to project it
            return get_linear_approx(start, end, efficiency)

        def get_second_load_pt(efficiency):
            start = max_index
            end = len(self.efficiency_data) - 1
            for i in range(max_index + 1, len(self.efficiency_data) - 2):
                if self.efficiency_data[i] <= efficiency:
                    end = i
                    break
                start += 1

            # if the point comes after the last value in the list, it will be able to project it
            return get_linear_approx(start, end, efficiency)

        min_perf_load = get_first_load_pt(min_perfect_eff)
        max_perf_load = get_second_load_pt(min_perfect_eff)

        min_good_load = get_first_load_pt(min_good_eff)
        max_good_load = get_second_load_pt(min_good_eff)

        return (
            (min_perf_load, max_perf_load),
            (min_good_load, max_good_load),
            self.load_data[max_index],
        )

    def should_increase(self, load):
        """
        Returns whether the current load should increase or decrease to obtain an optimal load.
        Any value before the max point should increase and vice-versa.
        """
        return load < self._optimal_load

    def is_perfect_eff(self, load):
        """
        Determines whether the given load lies within the perfect range.
        """
        return self._perfect_range[0] <= load <= self._perfect_range[1]

    def is_good_eff(self, load):
        """
        Determines whether the given load lies within the good range.
        """
        return self._good_range[0] <= load <= self._good_range[1]

    def get_cell_status(self, load):
        """
        See `get_efficiency_status()`
        """
        sign = -1 if self.should_increase(load) else 1
        if self.is_perfect_eff(load):
            return sign * 1
        elif self.is_good_eff(load):
            return sign * 2
        else:
            return sign * 3

    def get_efficiency_status(self, load_a, load_b):
        """
        Determine the efficiency status of the two fuel cells based on the csv file provided by
        the manufacturer. For each fuel cell, we will get an integer value between -3 and 3 (incl).
        The sign of a cell's output determines whether its load is below (negative) or over
        (positive) the optimal efficiency value. The absolute value of the output indicates in
        which range the value is currently lying:
          - 1: perfect (within the threshold)
          - 2: good (within 5 times the threshold)
          - 3: poor (over 5 times the threshold)
        This function will never return a value of zero, but will instead return 1 if the current
        load yields exactly the optimal status.
        """
        return self.get_cell_status(load_a), self.get_cell_status(load_b)


if __name__ == "__main__":
    se = SystemEfficiency("../data/eff_curves.csv")

    # simple tests for the `SystemEfficiency` class
    try:
        test_values = [
            (-10, 0),
            (19.8, 20000),
            (1326.46, 5486.008),
            (110.08, 709.8),
            (2000, 4000),
        ]
        expected_results = [(-3, -3), (-3, 3), (1, 2), (-3, -1), (1, 2)]

        for t, e in zip(test_values, expected_results):
            test_result = se.get_efficiency_status(*t)
            if test_result != e:
                print(f"Left: {test_result}. Right: {e}")
                raise Exception

        print("Tests succeeded!")
    except Exception:
        print("Tests failed.")
