#MUNDIAL Dos rangos (Unir csv)
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
from scipy.stats import t
import csv
from csv import*
import datetime
from math import*


total_laminas_album=640
costo_unidad=400
holograficas=40
especiales=40


#Funcion que define si el cuadrito dentro del album esta ocupado o no 
def espacio_lleno(i,album):
    if album[i] == 0:
        return False
    else:
        return True


#Funcion que define el costo total de llenar un album, teniendo en cuenta que aunque las laminas salgan repetidas no se pueden intercabiar
def c_album(total_laminas_album,costo_unidad):
    album=zeros(total_laminas_album)
    unidades_compradas=0
    repetidas=0
    no_repetidas=0
    costo_total=0
    while no_repetidas < total_laminas_album:
        lamina=randrange(0,total_laminas_album)
        if espacio_lleno(lamina,album)== False:
            album[lamina]=1
            costo_total+=costo_unidad
            no_repetidas+=1 
        else:
            costo_total+=costo_unidad
            repetidas+=1
    unidades_compradas=repetidas+no_repetidas
    #print unidades_compradas
    #print album
    return costo_total

# <codecell>

albums_a_llenar=arange(10,1000,10)
numero_de_albums=len(albums_a_llenar)

Valor_E_X=zeros(numero_de_albums)
Varianza_X=zeros(numero_de_albums)

# <codecell>

#Encuentra el valor esperado y la varianza dependiendo del tamano de muestra (numero de albums a llenar)
for j in range(0,numero_de_albums):
    print j
    vector_aux=zeros(albums_a_llenar[j])
    for i in range(0,albums_a_llenar[j]):
        vector_aux[i]=c_album(total_laminas_album,costo_unidad)
    Valor_E_X[j]=mean(vector_aux)
    Varianza_X[j]=var(vector_aux)

# <codecell>

#Verificamos si se llenaron lo vectores
print Valor_E_X
print Varianza_X

# <codecell>

#El metodo funciona para una cantidad pequeña pero para muestras grandes se demora demasiado. En teoria de 10 en 10 se podria demorar alrededor de 3 dias, es por esto que deje corriendo el programa por 2 dias en compufisica desde 1000 hasta 10000 de 50 en 50. Con el fin de ahorrar tiempo se genera un .csv para ambas situaciones

# <codecell>

#Se crea el csv para usar en futuras ocasiones
csv_out = open('CostoAlbumMundial10_1000_10.csv', 'wb')

Costos = csv.writer(csv_out)

for row in zip(albums_a_llenar, Valor_E_X, Varianza_X):
    Costos.writerow(row)

csv_out.close()

# <codecell>

#Para futuras ocasiones dado que correr el archivo es un demorado (alrededor de 30 min) se abre el archivo
albumsallenar10, ValorEX10, VarianzaX10= genfromtxt("CostoAlbumMundial10_1000_10.csv", delimiter=",", unpack=True)


#El metodo con el cual se realizo el CostoAlbumMundial1000_100000_50.csv se encuentra en un .py adjunto, el correr el archivo se demora mucho tiempo (2 dias) Mundial50.py


#Para futuras ocasiones dado que correr el archivo es un demorado (alrededor de 30 min) se abre el archivo
albumsallenar50, ValorEX50, VarianzaX50= genfromtxt("CostoAlbumMundial1000_100000_50.csv", delimiter=",", unpack=True)

albumsallenar=list(albumsallenar50)+list(albumsallenar10)
ValorEX=list(ValorEX10)+list(ValorEX50)
VarianzaX=list(VarianzaX10)+list(VarianzaX50)

#Grafica el tamano de muestra contra el valor esperado y la varianza del costo total (X)
fig, ax1 = subplots()

ax2 = ax1.twinx()
ax1.plot(albumsallenar, ValorEX, 'g-')
ax2.plot(albumsallenar, VarianzaX, 'b--')

title(u"Valor Esperado y Varianza del Costo Total")
ax1.set_xlabel('Numero de Albums a llenar')
ax1.set_ylabel('Valor esperado', color='g')
ax2.set_ylabel('Varianza', color='b')

show()

a= mean(ValorEX)
b=sqrt(mean(VarianzaX))

#Resutultado basandose en los .csv anteriores
print "R// Lo que cuesta llenar el album es", a, "junto con un error estandar de aproximadamente", b


#Referencias
    #http://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib
    #http://www.whit.com.au/blog/2011/11/reading-and-writing-csv-files/
    #https://www.wakari.io/sharing/bundle/bultako/CursoPythonCientifico


# b) Cual es el tamano de muestra m que se necesita para obtener 95 % de confianza en que |μm − μ| ≤ 10⁻⁶

#Se realiza el primedio de los valores esperados μm
Valor_prom_E=mean(ValorEX)

#El absoluto de la diferencia entre la Media_mu y los valores esperados de X 
Diferencial=abs(Valor_prom_E-ValorEX)


#Se realiza la grafica de los tamaños de muestra vs el diferencial
plot(albums_a_llenar,Diferencial)
yscale('log')
title(u"Valor Esperado y Varianza del Costo Total")
xlabel('Numero de Albums a llenar')
ylabel('Diferencial entre la media del Valor E y cada Valor E')
show()

print "R//No converge al valor esperado, dado que se conoce sigma y a media pero no se conoce el tipo de distribucion de los datos para hallar un tamaño de muestra dado un alfa de 0,05"


#Referencias
    #https://www.wakari.io/sharing/bundle/bultako/CursoPythonCientifico

# //////

# c) Ahora la probabilidad de obtener una lamina es diferente: $Pholograficas$= 1/3 $Pnormal$,  $Pespeciales$= 1/6 $Pnormal$


def seleccionar_lamina():
    items  = [["normal", 0.667], ["holografica", 0.222], ["especial", 0.111]]
    elems = [i[0] for i in items]
    probs = [i[1] for i in items]
    
    Lamina_S=numpy.random.choice(elems, 1, p=probs)
    #print Lamina_S
    return Lamina_S


def c_album_prob(total_laminas_album,costo_unidad,numero_a_llenar,holograficas,especiales):
    
    costo_total_X=zeros(numero_a_llenar)
    
    for i in range(0,numero_a_llenar):
        no_repetidas=0
        costo_total=0
        subtotal=total_laminas_album-holograficas-especiales
        album_n=zeros(subtotal)
        album_h=zeros(holograficas)
        album_e=zeros(especiales)
        
        while no_repetidas < total_laminas_album:
            L_S=seleccionar_lamina()
            
            if L_S=="normal":
                lamina=randrange(0,subtotal)
                if espacio_lleno(lamina,album_n)== False:
                    album_n[lamina]=1
                    costo_total+=costo_unidad
                    no_repetidas+=1 
                    
            if L_S=="holografica":
                lamina=randrange(0,holograficas)
                if espacio_lleno(lamina,album_h)== False:
                    album_h[lamina]=1
                    costo_total+=costo_unidad
                    no_repetidas+=1 
                    
            if L_S=="especial":
                lamina=randrange(0,especiales)
                if espacio_lleno(lamina,album_e)== False:
                    album_e[lamina]=1
                    costo_total+=costo_unidad
                    no_repetidas+=1 
                
            else:
                costo_total+=costo_unidad
        
        
        costo_total_X[i]=costo_total
    return costo_total_X

# <codecell>

u=c_album_prob(total_laminas_album,costo_unidad,1,holograficas,especiales) #1
d=c_album_prob(total_laminas_album,costo_unidad,10,holograficas,especiales) #10
c=c_album_prob(total_laminas_album,costo_unidad,100,holograficas,especiales) #100
m=c_album_prob(total_laminas_album,costo_unidad,1000,holograficas,especiales) #1000
dm=c_album_prob(total_laminas_album,costo_unidad,10000,holograficas,especiales) #10000

# <codecell>

#Csv que demuestra que el metodo anterior si genera los costos estimados de llenar el album
csv_out = open('CostoAlbumMundial_probabilidades_Funciona.csv', 'wb')

Costos = csv.writer(csv_out)

for row in zip(u, d, c, m, dm):
    Costos.writerow(row)

csv_out.close()

print datetime.datetime.now()


#Encuentra el valor esperado y la varianza dependiendo del tamano de muestra (numero de albums a llenar)
albums_a_llenar_10=arange(10,100,10)
albums_a_llenar_100=arange(100,1000,100)
albums_a_llenar_1000=arange(1000,10000,1000)
albums_a_llenar_10000=arange(10000,100000,10000)

numero_de_albums_1=len(albums_a_llenar_10)+len(albums_a_llenar_100)
numero_de_albums_2=len(albums_a_llenar_10)+len(albums_a_llenar_100)+len(albums_a_llenar_1000)
numero_de_albums_T=len(albums_a_llenar_10)+len(albums_a_llenar_100)+len(albums_a_llenar_1000)+len(albums_a_llenar_10000)

Valor_E_X=zeros(numero_de_albums_T)
Varianza_X=zeros(numero_de_albums_T)


for j in range(0,numero_de_albums_T):
    print j
    if j<len(albums_a_llenar_10):
        s=c_album_prob(total_laminas_album,costo_unidad,albums_a_llenar_10[j])
    if j>=len(albums_a_llenar_10) and j<numero_de_albums_1:
        s=c_album_prob(total_laminas_album,costo_unidad,albums_a_llenar_100[j-9])
    if j>=numero_de_albums_1 and j <numero_de_albums_2:
        s=c_album_prob(total_laminas_album,costo_unidad,albums_a_llenar_1000[j-18])
    if j>=numero_de_albums_2:
        s=c_album_prob(total_laminas_album,costo_unidad,albums_a_llenar_10000[j-27])
    Valor_E_X[j]=mean(s)
    Varianza_X[j]=var(s)


muestraNP= list(albums_a_llenar_10) + list(albums_a_llenar_100) + list(albums_a_llenar_1000) + list(albums_a_llenar_10000)
#print muestra

csv_out = open('CostoAlbumMundial_36it_noequiprobable.csv', 'wb')

Costos = csv.writer(csv_out)

for row in zip(muestra, Valor_E_X, Varianza_X):
    Costos.writerow(row)

csv_out.close()

#GRAFICA VAR-EXP

fig, ax1 = subplots()

ax2 = ax1.twinx()
ax1.plot(albumsallenarNP, ValorEXNP, 'g-')
ax2.plot(albumsallenarNP, VarianzaXNP, 'b--')

title(u"Valor Esperado y Varianza del Costo Total")
ax1.set_xlabel('Numero de Albums a llenar')
ax1.set_ylabel('Valor esperado', color='g')
ax2.set_ylabel('Varianza', color='b')

show()


#Se realiza el primedio de los valores esperados μm
Valor_prom_E=mean(ValorEXNP)

#El absoluto de la diferencia entre la Media_mu y los valores esperados de X 
Diferencial=abs(Valor_prom_ENP-ValorEXNP)


#Se realiza la grafica de los tamaños de muestra vs el diferencial
plot(albums_a_llenar,Diferencial)
yscale('log')
title(u"Valor Esperado y Varianza del Costo Total cuando es no Equiprobable")
xlabel('Numero de Albums a llenar')
ylabel('Diferencial entre la media del Valor E y cada Valor E')
show()

#REFERENCIAS
    #http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
