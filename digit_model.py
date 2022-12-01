import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    y_train = tf.keras.utils.to_categorical(y_train)
    y_test = tf.keras.utils.to_categorical(y_test)
    
    cnn_layers = []
    cnn_layers.append(tf.keras.Input(shape=(28, 28, 1)))
    cnn_layers.append(tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Flatten())
    cnn_layers.append(tf.keras.layers.Dense(128, activation='relu'))
    cnn_layers.append(tf.keras.layers.Dropout(0.15))
    cnn_layers.append(tf.keras.layers.Dense(64, activation='relu'))
    cnn_layers.append(tf.keras.layers.Dense(10, activation='softmax'))

    cnn_model = tf.keras.Sequential(cnn_layers)

    cnn_model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    n_epochs = 10
    history = cnn_model.fit(x_train.reshape(-1, 28, 28 ,1), y_train, epochs=n_epochs, validation_data=(x_test.reshape(-1, 28, 28 ,1), y_test))

    cnn_model.save('./digit_model.h5', save_format='h5')




if __name__ == "__main__":
    main()