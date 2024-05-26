# -*- coding: utf-8 -*-
"""Customer_churn_pred.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_jr_-UM4ZcYBu0qKf2LIP3g4wU6C_mAZ
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

df = pd.read_csv('/content/Churn_Modelling.csv')

df.head(10)

#lets do standardization so that now all values will range from 0 to 1
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

df.isnull().sum() #we have no missing values here

df.duplicated().sum() #no duplicate rows:

df.drop(columns=['RowNumber','CustomerId','Surname'],inplace = True)

df.head(10)

"""
get_dummies is a function in the pandas library in Python that converts categorical variables into dummy/indicator variables. This process is also known as one-hot encoding. One-hot encoding transforms categorical data into a format that can be provided to machine learning algorithms to improve predictions.

When you have categorical data, machine learning algorithms can't directly work with these categories. They need numerical values to perform calculations. get_dummies helps by creating binary (0 or 1) columns for each category level."""

# Convert categorical variables to dummy variables
df= pd.get_dummies(df, columns=['Geography', 'Gender'], drop_first=True).astype(int)

df

x = df.drop(columns=['Exited'])
y = df['Exited']


x_train,x_test,y_train,y_test =  train_test_split(x,y,test_size=0.2,random_state=1)

x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

x_train_scaled

import tensorflow
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

model = Sequential()

"""
Sure! Let's break down the code you provided, which defines two layers of a neural network using the Keras library in Python:

1. model.add(Dense(3, activation='sigmoid', input_dim=11))
Dense Layer: This is a fully connected layer, meaning each neuron in this layer is connected to every neuron in the previous layer.
3: The number of neurons in this layer. So this layer will have 3 neurons.
activation='sigmoid': The activation function used is the sigmoid function. This function outputs a value between 0 and 1 for each neuron, which is useful for binary classification tasks or for introducing non-linearity to the model.
input_dim=11: This specifies that the input to the model will have 11 features. This argument is only needed for the first layer of the model to define the shape of the input data.
2. model.add(Dense(1, activation='sigmoid'))
Dense Layer: Again, a fully connected layer.
1: The number of neurons in this layer. So this layer will have 1 neuron.
activation='sigmoid': The activation function used is the sigmoid function. Since this is the output layer and it has one neuron, this setup is typically used for binary classification tasks, where the output is a probability value between 0 and 1.
"""

#input layer,hidden layer,outplut layer


model.add(Dense(11,activation = 'relu',input_dim=11))
model.add(Dense(11,activation = 'relu'))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

history = model.fit(x_train_scaled,y_train,epochs=100,validation_split=0.2)

model.layers[0].get_weights()

model.layers[1].get_weights()

ylog=model.predict(x_test_scaled)

"""#as we are using sigmoid fuunction which will give us probablity whoose value is between 0 ad 1. so we decide a treshold ."""

y_pred = np.where(ylog>0.5,1,0)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

"""to improve accuracy we can increase no of epochs,activatio function = relu,hidden layers no of node increase...... its totally experimental"""

history.history

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])