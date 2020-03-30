# Instalación de paquetes adicionales
'''
!pip install dnspython
!pip install pymongo[srv]
!pip install numpy
!pip install surprise
'''

from pymongo import MongoClient
from google.colab import files
from surprise import Dataset, Reader, SVD, NormalPredictor
from surprise.model_selection import GridSearchCV
from google.colab import files
import io
import operator
import pandas as pd
import random
import numpy as np
import csv

# conexión
con = MongoClient('mongodb+srv://inmanueld:securepass@ps4games-8q85r.mongodb.net/test?retryWrites=true&w=majority')
db = con.ps4

games = db.game2.find()
users = db.user.find()

'''
for i in games:
  print("juego: ", i)
'''

'''
for i in users:
  print("usuario: ", i.get('email'))
'''

#print("#juegos: ",games.count())
#print("#usuarios: ", users.count())

# GENERAR EL .CSV

with open('games.csv', 'w', newline='', encoding='utf-8') as file:

  writer = csv.writer(file)

  for i in games:

    users_added = []
    game = i.get('title')

    if(len(i.get('rate')) > 0):
      rates_l = i.get('rate')
      for j in rates_l:
        if (j.get('email') not in users_added):
          writer.writerow([j.get('email'), game, j.get('calificacion')])
          users_added.append(j.get('email'))

      users = db.user.find()
      for l in users:
        if (l.get('email') not in users_added):
          writer.writerow([l.get('email'), game, 0])
      
    if (i.get('rate') == []):  
      users = db.user.find()
      for l in users:
        writer.writerow([l.get('email'), game, 0])

print("archivo games.csv generado!")
files.download('games.csv')

# ENTRENAMIENTO DEL MODELO
# leer el .csv, entrenar el modelo 

uploaded = files.upload()
df2 = pd.read_csv(io.BytesIO(uploaded['games.csv']))
reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(df2, reader)

df2

param_grid = {
    'n_epochs': [5, 10, 20, 50, 100],
    'lr_all': [0.002, 0.005],
    'reg_all': [0.4, 0.6]
}

gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data)

print(gs.best_score['rmse'])
print(gs.best_params['rmse'])

svd = SVD(n_epochs=100, lr_all=0.005, reg_all=0.4)
trainingSet = data.build_full_trainset()

svd.fit(trainingSet)

print("modelo entrenado!")

# PREDICCIONES SOBRE EL MODELO 
# hacer predicciones

users = db.user.find()

predictions = {}
games = []

user_email = input("Ingrese el correo del usuario al cual predecir:")

print('')
print("PREDICCIONES PARA EL USUARIO CON EMAIL: ", user_email)
print('')

games = db.game2.find()
for i in games:
  if(len(i.get('rate')) > 0):
    rates_l = i.get('rate')
    rates_email = []
    for j in rates_l:
      rates_email.append(j.get('email'))

    if (user_email not in rates_email):
      prediction = svd.predict(user_email, i.get('title'))
      predictions[i.get('title')] = prediction.est

c = 1

pred_sort = sorted(predictions.items(), key=operator.itemgetter(1), reverse=True)
for p in enumerate(pred_sort):
    print(c, '- ', p[1][0], 'has the prediction: ', predictions[p[1][0]])
    c+=1
    if (c == 11):
      break;