import csv
class SystemEfficiency:
    def __init__(self, csv_data_path):
        with open(csv_data_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=',')
            self.eff_curve = {row[0]: row[1:] for row in reader}
            self.opt_eff_point = {key: max(value) for key, value in self.eff_curve.items()}

    def _nearest_eff_points(self, fc_w):
        """
        Returns the two points on the efficiency curve that are closest to the current power output.
        """
        def find_closest_indices(arr, k):
            left = 0
            right = len(arr) - 1
            min_diff = float('inf')
            closest_indices = []

            while left < right:
                diff = abs(arr[left] - k)
                if diff < min_diff:
                    min_diff = diff
                    closest_indices = left, right

                if arr[right] == k:
                    return right, right

                if arr[right] < k:
                    return closest_indices

                if arr[left] == k:
                    return left, left

                if arr[left] > k:
                    return closest_indices

                if arr[right] - k < k - arr[left]:
                    left += 1
                else:
                    right -= 1
            return closest_indices
        
        pt_a_idx, pt_b_idx = find_closest_indices(self.eff_curve["e_load"], fc_w)
        pt_a = (self.eff_curve["e_load"][pt_a_idx], self.eff_curve["fc_efficiency"][pt_a_idx])
        pt_b = (self.eff_curve["e_load"][pt_a_idx], self.eff_curve["fc_efficiency"][pt_b_idx])
        return pt_a, pt_b

    
    def _interpolate(self, fc_w):
        pass

    def get_efficiency(self, fc_a_w, fc_b_w):
        pass

    def get_efficiency_status(self, efficiency, thres=0.05):
        pass

if __name__ == "__main__":
    se = SystemEfficiency("../data/eff_curves.csv")
