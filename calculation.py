import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot 


D90 = 0.22 * (10**-3) * (10**4)  # изначально 0.22 мДж/см2
l_milk = 20 * 10**-6



def function_to_integrate(D, d, r):
    a = -np.log(10)*D/D90
    b = -np.log(10)/l_milk

    return np.exp(a*np.exp(b*(r-d/2)))*r

def gamma(D, d, delta):
    upper_limit = d/2 + delta
    lower_limit = d/2

    coefficient = 2 / (delta*(d+delta))

    (value, error) = integrate.quad(lambda r: function_to_integrate(D, d, r), lower_limit, upper_limit)
    return 1 - coefficient*value


d = 0.4
delta = 200*10**-6

# eta1 = (1/3600)*(1/1000)*(1/1000)*Ds[0]*(d/((d+deltas)*deltas))*(1/0.05)

tau = 5*60
Qv = 10*(10**-3)/60

l = 0.3
S = np.pi*delta*(d+delta)
V_reactor = S*l
V_sum = 10**-3

f = 5
T = 1/f


Vel = Qv/S

n_reactor = (l/Vel)/T
print(n_reactor)

# D = [10*D90, 100*D90, 1000*D90, 10000*D90]
D = np.arange(D90, 250*D90, D90)

gammas_reactor = [gamma(x*n_reactor, d, delta) for x in D]

n = [np.log(0.1)/np.log(1-(V_reactor/V_sum)*gamma)*n_reactor*T for gamma in gammas_reactor]

eta = [(1/3600)*(1/1000)*(1/1000)*D[i]*n_reactor*n[i]*(d/((d+delta)*delta))*(1/0.05)*7 for i in range(len(D))]

result = f'd: {d*1000} мм, delta: {round(delta*1000000)} мкм, l: {l*100} см, f: {f} Гц'



# print(f'd: {d}, delta: {delta*10**6}, Степень витаминизации: {gammas[-1]}, Цена, рубли: {eta[-1]*7}')
fig, ax1 = pyplot.subplots()
ax1.set_xlabel('D/D90')
ax1.set_ylabel('Число циклов, n', color='tab:red')
ax1.plot([dd/D90 for dd in D], n, color='tab:red')
ax1.grid(visible=True)

ax2 = ax1.twinx()

# ax1.set_xlabel('D/D90')
ax2.set_ylabel('Стоимость, руб.', color='tab:pink')
ax2.plot([dd/D90 for dd in D], eta, color='tab:pink')

fig.tight_layout()
# pyplot.grid(visible=True)
# pyplot.text(10, 10, result, fontsize = 14, bbox = dict(facecolor = 'red', alpha = 0.5))
print(result)
pyplot.show()


# pyplot.legend(loc="best", prop={'size': 15})
# pyplot.grid(visible=True)
# # pyplot.yscale('log')
# # pyplot.xscale('log')
# pyplot.show()
