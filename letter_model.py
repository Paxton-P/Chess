import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import emnist

def main():
    emnist.ensure_cached_data()

    # Load emnist letter training data and restrict it to be only A-H
    (x_train, y_train) = emnist.extract_training_samples('letters')
    train_mask = np.logical_and(y_train < 9, y_train > 0)
    x_train = x_train[train_mask,]
    y_train = y_train[train_mask]

    # Load emnist letter testing data and restrict it to be only A-H
    (x_test, y_test) = emnist.extract_test_samples('letters')
    test_mask = np.logical_and(y_test < 9, y_test > 0)
    x_test = x_test[test_mask,]
    y_test = y_test[test_mask]

    # Convert y_train and y_test to categorical
    y_train = tf.keras.utils.to_categorical(y_train)
    y_test = tf.keras.utils.to_categorical(y_test)
    
    # Set up CNN architecture
    cnn_layers = []
    cnn_layers.append(tf.keras.Input(shape=(28, 28, 1)))
    cnn_layers.append(tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'))
    cnn_layers.append(tf.keras.layers.MaxPool2D())
    cnn_layers.append(tf.keras.layers.Flatten())
    cnn_layers.append(tf.keras.layers.Dense(9, activation='softmax'))

    # Define model based on that architecture
    cnn_model = tf.keras.Sequential(cnn_layers)

    # Compile and train model
    cnn_model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])
    n_epochs = 10
    history = cnn_model.fit(x_train.reshape(-1, 28, 28 , 1), y_train, epochs=n_epochs, validation_data=(x_test.reshape(-1, 28, 28 ,1), y_test))

    # Save the model for use in main.py
    cnn_model.save('./letter_model.h5', save_format='h5')




if __name__ == "__main__":
    main()
