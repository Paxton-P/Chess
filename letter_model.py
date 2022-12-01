import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import emnist

def main():

    (x_train, y_train) = emnist.extract_training_samples('letters')
    (x_test, y_test) = emnist.extract_test_samples('letters')

    # y_train = tf.keras.utils.to_categorical(y_train)
    # y_test = tf.keras.utils.to_categorical(y_test)

    print(y_train.shape)
    print(x_train.shape)
    
    cnn_layers = []
    cnn_layers.append(tf.keras.Input(shape=(28, 28, 1)))
    cnn_layers.append(tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Flatten())
    cnn_layers.append(tf.keras.layers.Dense(27, activation='softmax'))

    cnn_model = tf.keras.Sequential(cnn_layers)

    cnn_model.compile(optimizer="adam", loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    n_epochs = 10
    history = cnn_model.fit(x_train.reshape(-1, 28, 28 , 1), y_train, epochs=n_epochs, validation_data=(x_test.reshape(-1, 28, 28 ,1), y_test))

    cnn_model.save('./letter_model.h5', save_format='h5')




if __name__ == "__main__":
    main()