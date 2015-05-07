import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import pyfits

def gauss_model(t,c,d,sigma,mu):
	return c + d*t + (1/(sigma*np.sqrt(2*math.pi)))*np.exp(-0.5*((t-mu)/sigma)**2)

def step_model(t, f, g, h, n, t_0):
    return f + g*t + h*(1+(2/math.pi)*np.arctan(n*(t-t_0)))

def linear_model(x_obs, a, b):
    return x_obs*b + a
#Lectura de archivos e importacion de datos

stepfit = np.zeros((1,7))
with open('./fits/step_fit.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        stepfit = np.vstack((stepfit, row))
        
stepfit = stepfit[2:, :]

gaussfit = np.zeros((1,6))
with open('./fits/gauss_fit.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        gaussfit = np.vstack((gaussfit, row))
        
gaussfit = gaussfit[2:, :]

time = np.loadtxt("./data/time_series.csv")

linearfit = np.zeros((1,4))
with open('./fits/linear_fit.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        linearfit = np.vstack((linearfit, row))
        
linearfit = linearfit[2:, :]

sdo = pyfits.open('./data/hmi.m_45s.magnetogram.subregion_x1y1.fits')
time = np.loadtxt("./data/time_series.csv")
data = sdo[0].data


rows = ['observacion', 'modelo', 'a', 'b', 'c', 'd', 'sigma', 'mu', 'f', 'g', 'h', 'n' , 't_0']

#Comparacion de likelihoods

for i in range(100):

	print i

	gauss_lklhood = float(gaussfit[i, -1])
	step_lklhood = float(stepfit[i, -1])
	linear_lklhood = float(linearfit[i, -1])

	if gauss_lklhood > step_lklhood and gauss_lklhood > linear_lklhood:
		observacion = gaussfit[i, 0]
		pixels = observacion.split('_')
		campo = data[:, pixels[0], pixels[1]]
		c = float(gaussfit[i, 1])
		d = float(gaussfit[i, 2])
		sigma = float(gaussfit[i, 3])
		mu = float(gaussfit[i, 4])

		row = [observacion, 'gauss', 'NA', 'NA', c, d, sigma, mu, 'NA', 'NA', 'NA', 'NA', 'NA']
		rows = np.vstack((rows, row))

		gauss_fit = gauss_model(time, c, d, sigma, mu)
		titulo = "Pixel " + observacion
		path = "./Graficas/"+ observacion +".png"
		informacion = "c = " + gaussfit[i, 1] + "\n" + "d = " + gaussfit[i, 2] + "\n" + "sigma = " + gaussfit[i, 3] + "\n" + "mu = " + gaussfit[i, 4] + "\n" + "likelihood = " + gaussfit[i, -1] + "\n" 

		fig = plt.figure()
		plt.plot(time, campo)
		plt.plot(time, gauss_fit)
		plt.title(titulo)
		plt.xlabel("Tiempo [Minutos]")
		plt.ylabel("Campo Magnetico [Gauss]")
		fig.text(1,1,informacion, verticalalignment='top', horizontalalignment='right')
		plt.savefig(path) 


	elif step_lklhood > gauss_lklhood and step_lklhood > linear_lklhood:
		observacion = stepfit[i, 0]
		pixels = observacion.split('_')
		campo = data[:,pixels[0], pixels[1]]
		f = float(stepfit[i, 1])
		g = float(stepfit[i, 2])
		h = float(stepfit[i, 3])
		n = float(stepfit[i, 4])
		t_0 = float(stepfit[i, 5])

		row = [observacion, 'step', 'NA', 'NA','NA', 'NA', 'NA', 'NA', f, g, h, n, t_0]
		rows = np.vstack((rows, row))

		#creacion de grafica

		step_fit = step_model(time, f, g, h, n, t_0)
		titulo = "Pixel " + observacion
		path = "./Graficas/"+ observacion +".png"
		informacion = "f = " + stepfit[i, 1] + "\n" + "g = " + stepfit[i, 2] + "\n" + "h = " + stepfit[i, 3] + "\n" + "n = " + stepfit[i, 4] + "\n" + "t_0 = " + stepfit[i, 5] + "\n"+ "likelihood = " + stepfit[i, -1] + "\n" 

		fig = plt.figure()
		plt.plot(time, campo)
		plt.plot(time, step_fit)
		plt.title(titulo)
		plt.xlabel("Tiempo [Minutos]")
		plt.ylabel("Campo Magnetico [Gauss]")
		fig.text(1,1,informacion, verticalalignment='top', horizontalalignment='right')
		plt.savefig(path) 

	else:
		observacion = linearfit[i, 0]
		pixels = observacion.split('_')
		campo = data[:,pixels[0], pixels[1]]
		a = float(linearfit[i, 1])
		b = float(linearfit[i, 2])

		row = [observacion, 'linear', a, b, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA']
		rows = np.vstack((rows, row))

		#creacion de grafica

		linear_fit = linear_model(time, a, b)
		titulo = "Pixel " + observacion
		path = "./Graficas/"+ observacion +".png"
		informacion = "a = " + linearfit[i, 1] + "\n" + "b = " + linearfit[i, 2] + "\n" + "likelihood = " + linearfit[i, -1] + "\n" 

		fig = plt.figure()
		plt.plot(time, campo)
		plt.plot(time, linear_fit)
		plt.title(titulo)
		plt.xlabel("Tiempo [Minutos]")
		plt.ylabel("Campo Magnetico [Gauss]")
		fig.text(1,1,informacion, verticalalignment='top', horizontalalignment='right')
		plt.savefig(path) 
		



path = "./fits/bestmodels.txt"

with open(path, "wb") as f:
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
	for line in rows:
		writer.writerow(line)    
					
f.close()		