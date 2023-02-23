import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import os

cwd = os.getcwd()
#-----------------------------------------------------------------
'''
archivo = cwd + "/vital_signs.csv"

vital_signs = pd.read_csv(archivo, index_col="timestamp",parse_dates=True)

#Calcula la frecuencia promedio por hora
heart_rate = vital_signs["heart_rate"].resample("1H").mean()
print(heart_rate)
'''
#-----------------------------------------------------------------
'''
archivo = cwd + "/patient_data.csv"
archivo2 = cwd +"/population_data.csv"

patient_data = pd.read_csv(archivo)
population_data = pd.read_csv(archivo2)

merge_data = pd.merge(patient_data,population_data,on="Zip Code")

#Agregar columna nueva al dataset
merge_data["Chroncic Condition %"] = merge_data["Chronic Condition Count"]/merge_data["Population"] * 100
print(merge_data)
'''
#-----------------------------------------------------------------
archivo = cwd + "/ecg_data.csv"
ecg_data = pd.read_csv(archivo)

time = ecg_data["time"]
signal = ecg_data["signal"]

descripcion = ecg_data["signal"].describe()
#print(descripcion)

promedio = np.mean(ecg_data.signal)
#print(promedio)

'''
print(ecg_data["signal"].head(50))
print(ecg_data["signal"].tail(50))
'''
#Segmentacion de la señal para buscar barrera que permita hallar los valores pico
promedio_dinamico = pd.DataFrame.rolling(ecg_data.signal,window=(100)).mean()
#print(promedio_dinamico)

promedio_dinamico = [promedio*1.2 if math.isnan(x) else (x*1.2) for x in promedio_dinamico]
#print(promedio_dinamico)

ecg_data["promedio_dinamico"] = promedio_dinamico

#Deteccion de picos

cont = 0
rango = []
maximosy = []
maximosx = []
for punto in ecg_data.signal:
    if (punto <= ecg_data.promedio_dinamico[cont]) and (len(rango)<1):
        cont+=1
    elif (punto > ecg_data.promedio_dinamico[cont]):
        rango.append(punto)
        cont+=1
    else:
        maximo = max(rango)
        maximosy.append(maximo)
        maximox = cont - len(rango) + rango.index(maximo)
        maximosx.append(maximox)

        rango = []
        cont+=1

dist = []
cont = 0
while cont < len(maximosx)-1:
    distancia = maximosx[cont+1] - maximosx[cont]
    distancia = distancia/100 #Dividiendo entre freq. de muestreo
    dist.append(distancia)
    cont+=1

bpm = 60/np.mean(dist)
print("BPM: ",round(bpm,1))


plt.plot(time,signal)
plt.plot(ecg_data.promedio_dinamico, color = "r")
plt.scatter(maximosx,maximosy,color="orange",label=bpm)
plt.xlabel("Time (s)")
plt.ylabel("ECG signal (mV)")
plt.title("ECG Signal Over Time")
plt.legend(loc=4,framealpha = 0.6)
plt.show()
