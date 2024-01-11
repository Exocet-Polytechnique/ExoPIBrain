import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
import csv

def get_data(file_path):
    x_data = []
    y_data = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        x_data = [float(v) for v in next(reader)[1:]] # the name of the first column is weird when loading the file
        for row in reader:
            if row[0] == "fc_efficiency":
                y_data = [float(v) for v in row[1:]]
                break

    return x_data, y_data

def compute_best_polynomial(x_data, y_data, degree):
    coefficients = np.polyfit(x_data, y_data, degree)
    def polynomial(x):
        return np.polyval(coefficients, x)

    return polynomial


if __name__ == "__main__":
    # run this script from the exopibrain directory
    x_data, y_data = get_data("./data/eff_curves.csv")
    cs = CubicSpline(x_data, y_data)
    polynomial = compute_best_polynomial(x_data, y_data, len(x_data))

    plt.scatter(x_data, y_data, label="data")

    test_px = np.linspace(0, 5500, 100)
    test_py = polynomial(test_px)
    plt.plot(test_px, test_py, label="polynomial")

    test_cx = np.linspace(0, 5500, 100)
    test_cy = cs(test_cx)
    plt.plot(test_cx, test_cy, label="cubic spline")

    plt.show()
