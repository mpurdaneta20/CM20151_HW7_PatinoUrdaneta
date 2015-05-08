import numpy as np
import pyfits
import matplotlib.pyplot as plt
import csv
import math

print "Haciendo ajuste gaussiano"

#Importacion de datos

sdo = pyfits.open('./data/hmi.m_45s.magnetogram.subregion_x1y1.fits')
time = np.loadtxt("./data/time_series.csv")
data = sdo[0].data

#Definicion de funcion que calcula el likelihood

def likelihood(y_obs, y_model):
	chi_squared = (1.0/2.0)*sum((y_obs-y_model)**2)
	return -chi_squared

#Definicion de la funcion del modelo

def gauss_model(t,c,d,sigma,mu, A):
	return c + d*t + (A/(sigma*np.sqrt(2*math.pi)))*np.exp(-0.5*((t-mu)/sigma)**2)

#Creacion del header del csv
rows = np.array(['observacion', 'c', 'd', 'sigma', 'mu', 'A', 'likelihood'])

#Se hace un meshgrid para no eliminar la anidaciion de un for
x = np.arange(138, 148, 1)
y = np.arange(235,245, 1)
g = np.meshgrid(x,y)
Pixel_x = g[0].ravel()
Pixel_y = g[1].ravel()


#se hace el ajuste usando MCMC
for k in range(100):

	print k			
	campo = data[:, Pixel_x[k], Pixel_y[k]]
	c_walk = np.empty((0))
	d_walk = np.empty((0))
	sigma_walk = np.empty((0))
	mu_walk = np.empty((0))
	A_walk = np.empty((0))
	l_walk = np.empty((0))
	
	c_walk = np.append(c_walk, np.random.random())
	d_walk = np.append(d_walk, np.random.random())
	sigma_walk = np.append(sigma_walk, np.random.random())
	mu_walk = np.append(mu_walk, np.random.random())
	A_walk = np.append(A_walk, np.random.random())
	
	y_init = gauss_model(time, c_walk[0], d_walk[0], sigma_walk[0], mu_walk[0], A_walk[0])
	l_walk = np.append(l_walk, likelihood(campo, y_init))
	n_iterations = 20000

	for i in range(n_iterations):
	    c_prime = np.random.normal(c_walk[i], 20) 
	    d_prime = np.random.normal(d_walk[i], 0.1)
	    sigma_prime = np.random.normal(sigma_walk[i], 1)
	    mu_prime = np.random.normal(mu_walk[i], 10)
	    A_prime = np.random.normal(A_walk[i], 1)
	
	    y_init = gauss_model(time, c_walk[i], d_walk[i], sigma_walk[i], mu_walk[i], A_walk[i])
	    y_prime = gauss_model(time, c_prime, d_prime, sigma_prime, mu_prime, A_prime)
	    
	    l_prime = likelihood(campo, y_prime)
	    l_init = likelihood(campo, y_init)
	    
	    alpha = l_prime-l_init
	    if(alpha>=0.0):
	        c_walk = np.append(c_walk, c_prime)
	        d_walk = np.append(d_walk, d_prime)
	        sigma_walk = np.append(sigma_walk, sigma_prime)
	        mu_walk = np.append(mu_walk, mu_prime)
	        A_walk = np.append(A_walk, A_prime)
	        l_walk = np.append(l_walk, l_prime)
	    else:
	        beta = np.random.random()
	        if(beta<=alpha):
	            c_walk = np.append(c_walk, c_prime)
	            d_walk = np.append(d_walk, d_prime)
	            sigma_walk = np.append(sigma_walk, sigma_prime)
	            mu_walk = np.append(mu_walk, mu_prime)
	            A_walk = np.append(A_walk, A_prime)
	            l_walk = np.append(l_walk, l_prime)
	        else:
	            c_walk = np.append(c_walk,c_walk[i])
	            d_walk = np.append(d_walk,d_walk[i])
	            sigma_walk = np.append(sigma_walk, sigma_walk[i])
	            mu_walk = np.append(mu_walk, mu_walk[i])
	            A_walk = np.append(A_walk, A_walk[i])
	            l_walk = np.append(l_walk, l_init)

	max_index = np.argmax(l_walk)
	likelihood_obs = str(l_walk[max_index])
	best_c = str(c_walk[max_index])
	best_d = str(d_walk[max_index])
	best_sigma = str(sigma_walk[max_index])
	best_mu = str(mu_walk[max_index])
	best_A = str(A_walk[max_index])
	observacion = str(Pixel_x[k]) + "_" + str(Pixel_y[k])
		
	row =  [observacion, best_c, best_d, best_sigma, best_mu, best_A, likelihood_obs]
	rows = np.vstack((rows, row))

#Se escribe el archivo con los datos obtenidos	
path = "./fits/gauss_fit.csv"

print "Creando archivo"

with open(path, "wb") as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
	for line in rows:
		writer.writerow(line)    
					
f.close()		

						
