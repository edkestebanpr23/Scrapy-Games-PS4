# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:56:47 2020

@author: Christian Camilo Guzmán Escobar
"""

import numpy as np
from pymongo import MongoClient
import math
import pandas as pd
#from bson import ObjectId

# conexión
con = MongoClient('mongodb+srv://inmanueld:securepass@ps4games-8q85r.mongodb.net/test?retryWrites=true&w=majority')
db = con.ps4

games = db.game.find()

"""
    Procedimiento: El código a continuación representa un Sistema de Recomendación basado en
    contenido usando la distancia Euclidiana. El método realizado es el mismo llevado a cabo
    en el taller 5 de SRIW
"""

#IMPORTANTE: La siguiente variable (@params: userEmail) es para ingresar el EMAIL del usuario en la sesión.
userEmail = 'diego@gmail.com'
#userEmail = 'camilo@gmail.com'
#userEmail = 'juan@gmail.com'
#userEmail = 'alejo@gmail.com'
#userEmail = 'maria@gmail.com'
#userEmail = 'ceci@gmail.com'

#Variables para crear la matriz Datos Preparados (@params: datosPreparados)
ids = []
Title = []
Publisher = []
Classification = []
Genre = []
Developer = []

#Datos para perfil usuario (@params: perfilUsuario)
TitleUser = []
PublisherUser = []
ClassificationUser = []
GenreUser = []
DeveloperUser = []
misCalificaciones = []

"""
    Procedimiento: Se extrae de la base de datos los juegos y se recorren, se obtienen las
    calificaciones y si el usuario ha calificado el juego se guarda la información en
    variables para formar la matriz perfilUsuario, de lo contrario se guarda la información
    en variables para formar la matriz datosPreparados.
    Al ser un SR basado en contenido, se omiten los juegos que no poseen carácteristicas
"""

#Datos de usuario
"""
    @params: userNoFlag es una bandera que se activa si el juego tiene una calificación 
    del usuario de esta manera no se guarda en los datos para la matriz de datos preparados
    y se evita que queden datos duplicados e imprecisos. 
"""
for i in games:
    userNoFlag = True
    iden = i.get('_id')
    title = i.get('title')
    publisher = i.get('publisher')
    classification = i.get('classification')
    genre = i.get('genre')
    developer = i.get('developer')
    rate = i.get('rate')
    if(publisher != None and classification != None and genre != None and developer != None):
        if(rate and type(rate) != 'NoneType'):
            for j in rate:
                if(j.get('email') == userEmail):
                    TitleUser.append(title)
                    PublisherUser.append(publisher)
                    ClassificationUser.append(classification)
                    GenreUser.append(genre)
                    DeveloperUser.append(developer)
                    misCalificaciones.append(int(j.get('calificacion')))
                    userNoFlag = False
            if(userNoFlag == True):
                ids.append(iden)
                Title.append(title)
                Publisher.append(publisher)
                Classification.append(classification)
                Genre.append(genre)
                Developer.append(developer)
        else:
            ids.append(iden)
            Title.append(title)
            Publisher.append(publisher)
            Classification.append(classification)
            Genre.append(genre)
            Developer.append(developer)
 
"""
    Procedimiento: Se guardan los datos de las carácteristicas Publisher, Classification,
    Genre y Developer en arreglos que contengan los valores de los anteriores sin repetir.
    Esto con la finalidad de crear la primera fila o cabecera de la matriz.
"""

publisherKeys1 = list(Publisher) + list(PublisherUser)
publisherKeys = pd.Series(publisherKeys1).drop_duplicates().tolist()

classKeys1 =  list(Classification) + list(ClassificationUser)
classKeys =  pd.Series(classKeys1).drop_duplicates().tolist()

genreKeys1 = list(Genre) + list(GenreUser)
genreKeys = pd.Series(genreKeys1).drop_duplicates().tolist()

devKeys1 = list(Developer) + list(DeveloperUser)
devKeys = pd.Series(devKeys1).drop_duplicates().tolist()

"""
    Procedimiento: Se crea una matriz con len(TitleUser) filas, es decir, la cantidad de 
    juegos que el usuario calificó y columnsSize columnas usando las anteriores variables,
    la suma de estas será el número de columnas de la matriz. Dicha matriz se inicializa con
    ceros (0) en todos sus campos. 
    Para actualizar la matriz se recorre el tamaño de las filas y se actualizan  si el usuario
    ha calificado el juego perteneciente a la fila, en este mismo procedimiento se múltiplica
    el valor de la casilla por la calificación del usuario, de esta forma se obtienen una 
    matriz que describe los gustos del usuario por cada juego de acuerdo con su importancia.
    Se crea tambien una matriz de una fila y columnsSize columnas y así se van sumando los
    valores de las columnas de la matriz anteriormente explicada
"""

#Perfil de usuario
columnsSize = len(publisherKeys) + len(classKeys) + len(genreKeys) + len(devKeys)
perfilUsuario = np.zeros((len(TitleUser), columnsSize))

perfilUsuarioSuma = np.zeros((1,columnsSize))

perfilUsuarioNormalizado = np.zeros((1,columnsSize))

for i in range(0,len(TitleUser)):
    pub = publisherKeys.index(PublisherUser[i])
    perfilUsuario[i][pub] = 1 * misCalificaciones[i]
    perfilUsuarioSuma[0][pub] = perfilUsuarioSuma[0][pub] + (1 * misCalificaciones[i])
    
    clas = len(publisherKeys) + classKeys.index(ClassificationUser[i])
    perfilUsuario[i][clas] = 1 * misCalificaciones[i]
    perfilUsuarioSuma[0][clas] = perfilUsuarioSuma[0][clas] + (1 * misCalificaciones[i])
    
    gen = len(publisherKeys) + len(classKeys) + genreKeys.index(GenreUser[i])
    perfilUsuario[i][gen] = 1 * misCalificaciones[i]
    perfilUsuarioSuma[0][gen] = perfilUsuarioSuma[0][gen] + (1 * misCalificaciones[i])
    
    dev = len(publisherKeys) + len(classKeys) + len(genreKeys) + devKeys.index(DeveloperUser[i])
    perfilUsuario[i][dev] = 1 * misCalificaciones[i]
    perfilUsuarioSuma[0][dev] = perfilUsuarioSuma[0][dev] + (1 * misCalificaciones[i])

"""
    Procedimiento: Para crear el perfil de usuario normalizado se suman todos los elementos
    de perfilUsuarioSuma y luego los valores de perfilUsuarioNormalizado serán los valores de
    perfilUsuarioSuma dividido la suma de estos.
"""

suma = np.sum(perfilUsuarioSuma)

for i in range(0, columnsSize):
    perfilUsuarioNormalizado[0][i] = (perfilUsuarioSuma[0][i])/(suma)

#Preparar datos no calificados
    
"""
    Procedimiento: Se crea una matriz de datos preparados siguiendo el mismo procedimiento
    anterior y a su vez se crea una matriz que guarda los valores de (Xi - Yi) en la
    formula de la distancia euclidiana.
    La matriz de datos preparados se llena de la misma manera como se llena la matriz de 
    perfil de usuario a diferencia que en esta en vez de multiplicar por la calificación del
    usuario se llena con un 1.
    La distancia euclidiana en la fila i inicialmente es el mismo perfi de usuario normalizado
    y luego se actualzan los valores en la columna donde hay una carácteristica en 1 de manera
    que queda el valor de perfil de usuario normalizado en la posición de la columna menos uno,
    esto es (Xi - Yi), en el caso en que no hay carácteristica esto es (Xi - 0) = Xi. Luego de
    esto se elevan al cuadrado los valores de los elementos y se suman.
    Por ultimo se crea un dicionario llamado distanciaEuclidiana2, el cual tiene los atributos
    "_idJuego" que es el id del juego en la bd, "title" que es el título del juego y 
    "recommendationScore" el cual es la raiz cuadrada de la suma anterior.
"""
    
columnsSize = len(publisherKeys) + len(classKeys) + len(genreKeys) + len(devKeys)
datosPreparados = np.zeros((len(Title), columnsSize))

distanciaEuclidiana = np.zeros((len(Title), columnsSize))
distanciaEuclidiana2 = []

for i in range(0,len(Title)):
    distanciaEuclidiana[i] = perfilUsuarioNormalizado
    
    pub = publisherKeys.index(Publisher[i])
    datosPreparados[i][pub] = 1
    distanciaEuclidiana[i][pub] = distanciaEuclidiana[i][pub] - 1
    
    clas = len(publisherKeys) + classKeys.index(Classification[i])
    datosPreparados[i][clas] = 1
    distanciaEuclidiana[i][clas] = distanciaEuclidiana[i][clas] - 1
    
    gen = len(publisherKeys) + len(classKeys) + genreKeys.index(Genre[i])
    datosPreparados[i][gen] = 1
    distanciaEuclidiana[i][gen] = distanciaEuclidiana[i][gen] - 1
    
    dev = len(publisherKeys) + len(classKeys) + len(genreKeys) + devKeys.index(Developer[i])
    datosPreparados[i][dev] = 1
    distanciaEuclidiana[i][dev] = distanciaEuclidiana[i][dev] - 1

    distanciaEuclidiana[i] = np.square(distanciaEuclidiana[i])
    sumOfDistEuclidiana = np.sum(distanciaEuclidiana[i])
    
    resultObject = { "_idJuego": str(ids[i]),"title": Title[i], "recommendationScore": math.sqrt(sumOfDistEuclidiana)}
    distanciaEuclidiana2.append(resultObject)
#    print(Title[i], '\n')

#Distancia Euclidiana
distanciaEuclidiana2.sort(key = lambda i: i['recommendationScore'])
recomendados = []
for i in range(0,9):
    recomendados.append(distanciaEuclidiana2[i])
    print(recomendados[i],'\n')   