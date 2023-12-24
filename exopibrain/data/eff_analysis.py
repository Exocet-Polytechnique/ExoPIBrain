import matplotlib.pyplot as plt
import numpy as np
import csv

if __name__ == "__main__":
    load = []
    values = {}

    with open("./eff_curves.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # the first row contains data about the electric load
        # but we want to remove the label ('e_load')
        load = [float(v) for v in next(reader)[1:]]
        for row in reader:
            values[row[0]] = [float(v) for v in row[1:]]

    for name, data in values.items():
        if name == "fc_efficiency":
            plt.plot(load, data)

    def get_approx_value(value, name):
        # 1. find range in which the value lies
        # start_index will be zero if the value comes before the given data
        start_i = 0
        # end_index will be the max point if the values lies beyond the given data
        end_i = len(load) - 1

        for i in range(1, len(load) - 1):
            if load[i] >= value:
                end_i = i
                break

            start_i = i

        # 2. determine the parameters of a linear function to map the values
        # this is similar to linear interpolation
        def linearize_func(x):
            data = values[name]
            m = (data[end_i] - data[start_i]) / (load[end_i] - load[start_i])
            b = data[start_i] - m * load[start_i]
            return m * x + b

        return linearize_func(value)

    x_vals = np.linspace(0, 5600, 40)
    y_vals = [get_approx_value(v, "fc_efficiency") for v in x_vals]
    plt.scatter(x_vals, y_vals)

    plt.show()
