import numpy as np
import pyfits
import matplotlib.pyplot as plt
import csv
import math

print "Haciendo ajuste de paso"

sdo = pyfits.open('./data/hmi.m_45s.magnetogram.subregion_x1y1.fits')
time = np.loadtxt("./data/time_series.csv")
data = sdo[0].data


def likelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*sum((y_obs-y_model)**2)
	return -chi_squared

def step_model(t, f, g, h, n, t_0):
    return f + g*t + h*(1+(2/math.pi)*np.arctan(n*(t-t_0)))

rows = np.array(['observacion', 'f', 'g', 'h', 'n', 't_0', 'likelihood'])

x = np.arange(138, 148, 1)
y = np.arange(235,245, 1)
g = np.meshgrid(x,y)
Pixel_x = g[0].ravel()
Pixel_y = g[1].ravel()



for k in range(100):

	print k
	campo = data[:, Pixel_x[k], Pixel_y[k]]
	f_walk = np.empty((0)) #this is an np.empty list to keep all the steps
	g_walk = np.empty((0))
	h_walk = np.empty((0))
	n_walk = np.empty((0))
	t_0_walk = np.empty((0))
	l_walk = np.empty((0))
	
	f_walk = np.append(f_walk, np.random.random())
	g_walk = np.append(g_walk, np.random.random())
	h_walk = np.append(h_walk, np.random.random())
	n_walk = np.append(n_walk, np.random.random())
	t_0_walk = np.append(t_0_walk, np.random.random())
	
	y_init = step_model(time, f_walk[0], g_walk[0], h_walk[0], n_walk[0], t_0_walk[0])
	l_walk = np.append(l_walk, likelihood(campo, y_init))
	n_iterations = 20000
	for i in range(n_iterations):
	    f_prime = np.random.normal(f_walk[i], 20) 
	    g_prime = np.random.normal(g_walk[i], 0.1)
	    h_prime = np.random.normal(h_walk[i], 10)
	    n_prime = np.random.normal(n_walk[i], 10)
	    t_0_prime = np.random.normal(n_walk[i], 10)
	
	    y_init = step_model(time, f_walk[i], g_walk[i], h_walk[i], n_walk[i], t_0_walk[i])
	    y_prime = step_model(time, f_prime, g_prime, h_prime, n_prime, t_0_prime)
	    
	    l_prime = likelihood(campo, y_prime)
	    l_init = likelihood(campo, y_init)
	    
	    alpha = l_prime-l_init
	    if(alpha>=0.0):
	        f_walk = np.append(f_walk, f_prime)
	        g_walk = np.append(g_walk, g_prime)
	        h_walk = np.append(h_walk, h_prime)
	        n_walk = np.append(n_walk, n_prime)
	        t_0_walk = np.append(t_0_walk, t_0_prime)
	        l_walk = np.append(l_walk, l_prime)
	    else:
	        beta = np.random.random()
	        if(beta<=alpha):
	            f_walk = np.append(f_walk, f_prime)
	            g_walk = np.append(g_walk, g_prime)
	            h_walk = np.append(h_walk, h_prime)
	            n_walk = np.append(n_walk, n_prime)
	            t_0_walk = np.append(t_0_walk, t_0_prime)
	            l_walk = np.append(l_walk, l_prime)
	        else:
	            f_walk = np.append(f_walk, f_walk[i])
	            g_walk = np.append(g_walk, g_walk[i])
	            h_walk = np.append(h_walk, h_walk[i])
	            n_walk = np.append(n_walk, n_walk[i])
	            t_0_walk = np.append(t_0_walk, t_0_walk[i])
	            l_walk = np.append(l_walk, l_init)
	max_index = np.argmax(l_walk)
	likelihood_obs = l_walk[max_index]
	best_f = f_walk[max_index]
	best_g = g_walk[max_index]
	best_h = h_walk[max_index]
	best_n = n_walk[max_index]
	best_t_0 = t_0_walk[max_index]
	observacion = str(Pixel_x[k]) + "_" + str(Pixel_y[k])
		
	row =  [observacion, best_f, best_g, best_h, best_n, best_t_0, likelihood_obs]
	rows = np.vstack((rows, row))

path = "./fits/step_fit.csv"

print "Creando archivo"

with open(path, "wb") as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
	for line in rows:
		writer.writerow(line)    
					
f.close()		