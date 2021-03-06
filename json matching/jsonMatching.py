# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:12:13 2020

@author: USER
"""

import Levenshtein
import json
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
""" from nltk.corpus import stopwords """

stopwords = ['limited','preorder','remake', 'ps4', 'playstation', 'with', 'day', 'one', 'gold','hits','premium', 'complete', 'champion', 'launch', 'pre-order', 'special', 'edition', 'bonus', 'dlc', 'preowned', 'remastered', 'xl', 'deluxe', 'enhanced', 'digital', 'apex', 'definitive', 'anniversary', 'standard', 'ultimate']
""" stopwords = stopwords.words('english') """

# conexión
print('Conectandose con base de datos')
con = MongoClient('mongodb+srv://inmanueld:securepass@ps4games-8q85r.mongodb.net/test?retryWrites=true&w=majority')
db = con.ps4
Games = db.game
resultado = Games.find()
juegos = []
#print(resultado)
for x in resultado:
   juegos.append(x)

print('Inicio de merge entre resultados encontrados, espere...') 
def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    
    return text

def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    
    return cosine_similarity(vec1, vec2)[0][0]    

with open('../games.json') as gamesJson:
    games = json.load(gamesJson)

with open('../buygames.json') as buygamesJson: 
    buyGames = json.load(buygamesJson)
               
for gameItem in games:
    sentences = []
    sentences.append(gameItem.get('title'))
    gameItem.update({"url2": None})
    for buyGameItem in buyGames:
        sentences.append(buyGameItem.get('title'))
        buyGameItem.update({"url2": None})
        buyGameItem.update({"publisher": None})
        buyGameItem.update({"classification": None})
        buyGameItem.update({"genre": None})
        buyGameItem.update({"developer": None})
        cleaned = list(map(clean_string, sentences))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        csim = cosine_sim_vectors(vectors[0], vectors[1])
        if(csim > 0.9):
            levDistance = Levenshtein.distance(cleaned[0], cleaned[1])
            if(levDistance == 0):
                gameItem.update({"url2": buyGameItem.get('url')})
                buyGames.pop(buyGames.index(buyGameItem))    
        sentences.pop(1)
    sentences.clear()
        


newGames = games

# Eliminando atributos de id y calificación para comparar con los juegos almacenados en DB
for item in juegos:
    if item.get('_id') != None:
        del item['_id']
    if item.get('rate') != None:
        del item['rate']
    if item.get('state') != None:
        del item['state']

# Comparando si los juegos encontrados ahora ya existen en DB o si ya dejaron de existir
aux_newGames = juegos
for item in newGames:
    if item in juegos:
        print('Existe el juego:', item['title'])
        del aux_newGames[aux_newGames.index(item)]
    else:
        item['rate'] = []
        item['state'] = True
        print('...:', item)
        Games.insert_one(item)

# Cambiando el estado a los juegos que dejaron de estar publicados
if len(aux_newGames) > 0:
    print('Hay items que dejaron de existir')
    for item in aux_newGames:
        print(item)
        Games.update_one({"title": item['title']}, { "$set": { 'state': False } })
        

# 
#mergedGames = games + buyGames
#with open('../mergedGames.json', 'w') as json_file:
#  json.dump(mergedGames, json_file)
#    
#for mergedItem in mergedGames:
#   Games.update_one({ "title": mergedItem.get('title')}, mergedItem)  
""" print(games) 
print(buyGames) """