import numpy as np
import pyfits
import matplotlib.pyplot as plt
import csv
import math

#Importacion de datos

sdo = pyfits.open('./data/hmi.m_45s.magnetogram.subregion_x1y1.fits')
time = np.loadtxt("./data/time_series.csv")
data = sdo[0].data

#Definicion de funcion que calcula el likelihood

def linear_likelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*sum((y_obs-y_model)**2)
	return -chi_squared

#Definicion de la funcion del modelo

def linear_model(x_obs, a, b):
    return x_obs*b + a

rows = np.array(['observacion', 'a', 'b', 'likelihood'])

x = np.arange(138, 148, 1)
y = np.arange(235,245, 1)
g = np.meshgrid(x,y)
Pixel_x = g[0].ravel()
Pixel_y = g[1].ravel()

for k in range(100):
	print k

	campo = data[:, Pixel_x[k], Pixel_y[k]]

	a_walk = np.empty((0))
	b_walk = np.empty((0))
	l_walk = np.empty((0))
	
	a_walk = np.append(a_walk, np.random.random())
	b_walk = np.append(b_walk, np.random.random())
	
	y_init = linear_model(time, a_walk[0], b_walk[0])
	l_walk = np.append(l_walk, linear_likelihood(campo, y_init))

	n_iterations = 20000
	for i in range(n_iterations):
	    a_prime = np.random.normal(a_walk[i], 20) 
	    b_prime = np.random.normal(b_walk[i], 0.1)
	
	    y_init = linear_model(time, a_walk[i], b_walk[i])
	    y_prime = linear_model(time, a_prime, b_prime)
	    
	    l_prime = linear_likelihood(campo, y_prime)
	    l_init = linear_likelihood(campo, y_init)
	    
	    alpha = l_prime-l_init
	    if(alpha>=0.0):
	        a_walk  = np.append(a_walk,a_prime)
	        b_walk  = np.append(b_walk,b_prime)
	        l_walk = np.append(l_walk, l_prime)
	    else:
	        beta = np.random.random()
	        if(beta<=alpha):
	            a_walk = np.append(a_walk,a_prime)
	            b_walk = np.append(b_walk,b_prime)
	            l_walk = np.append(l_walk, l_prime)
	        else:
	            a_walk = np.append(a_walk,a_walk[i])
	            b_walk = np.append(b_walk,b_walk[i])
	            l_walk = np.append(l_walk, l_init)

	max_index = np.argmax(l_walk)
	likelihood_obs = str(l_walk[max_index])
	best_a = a_walk[max_index]
	best_b = b_walk[max_index]
	observacion = str(Pixel_x[k]) + "_" + str(Pixel_y[k])

	row =  [observacion, best_a, best_b, likelihood_obs]
	rows = np.vstack((rows, row))

path = "./fits/linear_fit.csv"

print "Creando archivo"

with open(path, "wb") as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
	for line in rows:
		writer.writerow(line)    
					
f.close()

