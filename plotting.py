from scipy.optimize import curve_fit
import numpy as np
from numpy import arange
from matplotlib import pyplot
from processing import get_data
import pickle

# reading zero values from pickle
with open('zero.pickle', 'rb') as file:
    read_data: dict = pickle.load(file)
    zero_abs_values = read_data["abs"]

def fit_abs(fat_percentage, concentrations, first_is_zero=False):
    data = get_data(fat_percentage, concentrations)

    # change for an experiment with no zeros to concentrations[:]
    concentrations = concentrations[1:] if first_is_zero else  concentrations


    lambdas = data[concentrations[0]]["lambda"]

    abs_fitted = []
        
    for value in lambdas:
        position = lambdas.index(value)
        if not first_is_zero:
            abs_values = [data[concentration]["abs"][position] - zero_abs_values[position] for concentration in concentrations]
        else:
            abs_values = [data[concentration]["abs"][position] - data[0]["abs"][position] for concentration in concentrations]
            
        
        # removing values that are too high to detect
        positions_to_remove = list(filter(lambda i: abs_values[i] <= 0, range(len(abs_values))))

        abs_without_limit = []
        concentrations_without_limit = []
        for i in range(len(abs_values)):
            if i not in positions_to_remove:
                abs_without_limit.append(abs_values[i])
                concentrations_without_limit.append(concentrations[i])
            
        if len(abs_without_limit) > 1:
            res, _ = curve_fit(f=lambda x, k: k*x, xdata=concentrations_without_limit, ydata=abs_without_limit)
            coefficient = res[0]
        else:
            coefficient = abs_without_limit[0] / concentrations_without_limit[0]
        
        abs_fitted.append(coefficient)

        # print(value)
        # pyplot.plot([0, 1], [0, coefficient])
        # pyplot.scatter(concentrations_without_limit, abs_without_limit, marker='o')
        # pyplot.xlim(0 - max(concentrations)/10, max(concentrations) + max(concentrations)/10)
        # pyplot.ylim(0, 2.1)
        # pyplot.grid(visible=True)
        # pyplot.show()
    
    return (lambdas, abs_fitted)


concentrations = [0, 1/40, 1/80, 1/160]
fat_percentage = '1.5'

# concentrations = [1/40, 1/80, 1/160]
# fat_percentage = '4.1'



print(*fit_abs(fat_percentage, concentrations))
fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
pyplot.ylim(0, 70)
pyplot.xlim(220, 350)
pyplot.plot(*fit_abs('1.5', [0, 1/40, 1/80, 1/160], first_is_zero=True), color='red', label='1.5')
pyplot.plot(*fit_abs('2.5', [1/40, 1/80, 1/160]), color='green', label='2.5')
pyplot.plot(*fit_abs('3.2', [1/40, 1/80, 1/160]), color='blue', label='3.2')
pyplot.plot(*fit_abs('4.1', [0, 1/40, 1/80, 1/160], first_is_zero=True), color='purple', label='4.1')
pyplot.legend(loc="best", prop={'size': 15})
pyplot.grid(visible=True)
ax.set_xticks(np.arange(220, 360, 10))
ax.set_xticks(np.arange(225, 365, 5), label='')
ax.set_yticks(np.arange(0, 80, 5))
# pyplot.yscale('log')
pyplot.show()
