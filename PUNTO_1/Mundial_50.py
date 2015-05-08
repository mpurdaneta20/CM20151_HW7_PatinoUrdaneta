# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Punto 1


# a) ¿Cuanto cuesta llenar el album del mundial?
# En una primera instancia se realiza la estimacion del valor esperado y la varianza con el fin de determinar el costo de llenar una cantidad finita de albums (m=10:100:10⁵) y la variabilidad de dicho costo.

from matplotlib import*
from pylab import*
from numpy import*
from random import*
import csv
from csv import*
import math
import datetime

total_laminas_album=640
costo_unidad=400

#Funcion que define si el cuadrito dentro del album esta ocupado o no; esta funcion se planeto en un principio pero 
def espacio_lleno(i,album):
    if album[i] == 0:
        return False
    else:
        return True


#Funcion que define el costo total de llenar un album, teniendo en cuenta que aunque las laminas salgan repetidas no se pueden intercabiar
def c_album(total_laminas_album,costo_unidad,numero_a_llenar):
    
    costo_total_X=zeros(numero_a_llenar)
    
    for i in range(0,numero_a_llenar):
        no_repetidas=0
        costo_total=0
        album=zeros(total_laminas_album)
        while no_repetidas < total_laminas_album:
            lamina=randrange(0,total_laminas_album)
            #if album[lamina]==0:
            if espacio_lleno(lamina,album)== False:
                album[lamina]=1
                costo_total+=costo_unidad
                no_repetidas+=1 
                
            else:
                costo_total+=costo_unidad
        
        
        costo_total_X[i]=costo_total
    return costo_total_X

#MUNDIAL Rango de 1000 a 100000 de 50 en 50.
#Prueba duracion del loop 
#print datetime.datetime.now()
#c_album(total_laminas_album,costo_unidad,1000)
#print datetime.datetime.now()


#Encuentra el valor esperado y la varianza dependiendo del tamano de muestra (numero de albums a llenar)
albums_a_llenar=arange(1000,100000,50)

numero_A=len(albums_a_llenar)

Valor_E_X=zeros(numero_A)
Varianza_X=zeros(numero_A)


for j in range(0,numero_A):
    print j
    s=c_album(total_laminas_album,costo_unidad,albums_a_llenar[j])
    
    Valor_E_X[j]=mean(s)
    Varianza_X[j]=var(s)

#Verificamos si se llenaron lo vectores
print Valor_E_X
print Varianza_X


muestra= albums_a_llenar
#print muestra

csv_out = open('CostoAlbumMundial1000_100000_50.csv', 'wb')

Costos = csv.writer(csv_out)

for row in zip(muestra, Valor_E_X, Varianza_X):
    Costos.writerow(row)

csv_out.close()






