import numpy as np
from PIL import Image

model = np.load("model.npz")
W1, W2 = model["W1"], model["W2"]
b1, b2 = model["b1"], model["b2"]

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    x = x - np.max(x, axis=1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=1, keepdims=True)

def preprocess(image):
    image = image.convert("L")          # grayscale

    image = image.resize((28, 28))

    img = np.array(image).astype(np.float32)

    img = img / 255.0
    img = 1.0 - img

    return img.reshape(1, 784)

def image_processing(image):
    x = preprocess(image)

    z1 = x @ W1 + b1
    a1 = relu(z1)

    z2 = a1 @ W2 + b2
    y_pred = softmax(z2)

    return int(np.argmax(y_pred))