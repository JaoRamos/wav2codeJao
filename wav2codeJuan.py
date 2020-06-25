# -*- coding: utf-8 -*-
'''
Script para leer un wav y convertirlo a codigo en (C?)
En principio convierte a un array de floats por cada muestra

Created on Tue Jun 23 11:06:14 2020
@author: jao
'''

import numpy as np
from datetime import date
from math import floor
from scipy.io.wavfile import read


# constantes de strings
L = "\n"    # salto de linea
T = "\t"
sep = ", "
archivo = "test.wav"  # convertir en argumento...
destino = archivo.split(".", 1)
destino = destino[0] + ".cpp"

# wavread de pablo -------------------------------
def wavread(file_name):
    fs, y = read(file_name)
    return fs, np.array(y.T, dtype=np.float64) / (2**15 - 1)

# crea el array de numeros ordenados como codigo C
def crearArrayC(datos, porLinea):
    resultado = "float datos [N_ELEMENTOS] = {\n\t"
    indice = 0
    
    # lo partimos en grupos de 8 por linea
    for x in range(floor( len(datos)/porLinea ) + 1):
        for i in range(porLinea):
            indice += 1
            if indice == len(datos):
                break
            # agregamos los valores
            resultado += str(datos[indice])
            if indice < len(datos)-1:     # excepto el ultimo!
                resultado += sep
        if x < floor( len(datos)/porLinea ):     # excepto ultima linea!
            resultado += "\n\t"     #salto de linea e indentacion
    
    resultado += "\n};"  # cierre final
    return resultado



# lee el archivo de audio y extrae los datos
sr, audio = wavread(archivo)
texto = crearArrayC(audio, 8)

# crea los strings generales
comienzo = "/*" +L
juan = "   Creado con wav2codeJuan (Jao Ramos 2020)" +L
fecha = date.today()
fechaStr = "   Fecha: " + fecha.strftime("%B %d, %Y") +L
nombre = "   Archivo: " + archivo +L
nSamples = "   Cantidad de samples: " + str(len(audio)) +L
rate = "   Sample Rate: " + str(sr) + " Hz" +L
cierre = "*/" +L +L
constante = "#define N_ELEMENTOS " + str(len(audio)) +L

salida = comienzo + juan + fechaStr + nombre + nSamples + rate + cierre + constante + L + texto

# escribe el archivo
archivoSalida = open(destino,"w") 
archivoSalida.write(salida) 
archivoSalida.close()
