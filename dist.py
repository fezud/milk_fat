import pickle
from matplotlib import pyplot

# reading zero values from pickle
with open('zero.pickle', 'rb') as file:
    read_data: dict = pickle.load(file)
    zero_abs_values = read_data["abs"]
    lambdas = read_data["lambda"]


pyplot.plot(lambdas, zero_abs_values, color='red', label='Дистиллят')
pyplot.legend(loc="best", prop={'size': 15})
pyplot.grid(visible=True)
pyplot.xlim(150, 1150)
pyplot.ylim(0, 2.5)
# pyplot.yscale('log')
pyplot.show()