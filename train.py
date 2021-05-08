import os
import numpy as np

from vae import VAE

LEARNING_RATE = 0.0005
BATCH_SIZE = 64
EPOCHS = 40

IMAGES_PATH = "dataset/groove2img_npy/"

def load_groove(dataset_path):
    x_train = []
    file_names = os.listdir(dataset_path)

    for file_name in file_names:
        if file_name.endswith('.npy'):
            file_path = os.path.join(dataset_path, file_name)
            g2i = np.load(file_path)
            x_train.append(g2i)

    x_train = np.array(x_train)
    x_train = x_train.astype("float32") / 255
    x_train = x_train.reshape(x_train.shape + (1,))

    print(x_train.shape)

    return x_train

def load_mnist():
    from tensorflow.keras.datasets import mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = x_train.astype("float32") / 255
    x_train = x_train.reshape(x_train.shape + (1,))
    x_test = x_test.astype("float32") / 255
    x_test = x_test.reshape(x_test.shape + (1,))

    print(x_train.shape)

    return x_train, y_train, x_test, y_test

def train(x_train, learning_rate, batch_size, epochs):
    autoencoder = VAE(
        #input_shape=(28, 28, 1),
        input_shape=(106, 100, 1),
        conv_filters=(32, 64, 64, 64),
        conv_kernels=(3, 3, 3, 3),
        conv_strides=(1, 1, 1, 2),
        latent_space_dim=2
    )
    autoencoder.summary()
    autoencoder.compile(learning_rate)
    autoencoder.train(x_train, batch_size, epochs)
    return autoencoder


if __name__ == "__main__":
    x_train = load_groove(IMAGES_PATH)
    #x_train = load_mnist()[:50]
    autoencoder = train(x_train, LEARNING_RATE, BATCH_SIZE, EPOCHS)
    autoencoder.save("model")