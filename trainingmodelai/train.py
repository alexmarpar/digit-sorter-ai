import numpy as np
from sklearn.datasets import fetch_openml

print("Cargando MNIST...")
mnist = fetch_openml("mnist_784", version=1, as_frame=False)

# -----------------------
# ACTIVATIONS
# -----------------------
def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

def softmax(x):
    # Truco de estabilidad numérica restando el max
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

# -----------------------
# LOAD DATA & NORMALIZE
# -----------------------
# Es crucial normalizar los píxeles de 0-255 a 0-1 para que las activaciones no exploten
x = mnist.data.astype(np.float32) / 255.0
y = mnist.target.astype(int)

split = 60000
x_train, x_test = x[:split], x[split:]
y_train, y_test = y[:split], y[split:]

# One hot
y_train_oh = np.eye(10)[y_train]
y_test_oh = np.eye(10)[y_test]

# -----------------------
# INIT WEIGHTS (He/Xavier-ish initialization)
# -----------------------
input_size = 784
hidden_size = 128
output_size = 10

# Multiplicar por un factor basado en el tamaño ayuda a que converja rápido
W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
b1 = np.zeros((1, hidden_size))

W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
b2 = np.zeros((1, output_size))

# -----------------------
# TRAINING CONFIG
# -----------------------
lr = 0.1
epochs = 5
batch_size = 128
num_samples = x_train.shape[0]

for epoch in range(epochs):
    # Mezclar los datos en cada época para un mejor entrenamiento
    permutation = np.random.permutation(num_samples)
    x_train_shuffled = x_train[permutation]
    y_train_oh_shuffled = y_train_oh[permutation]
    
    epoch_loss = 0
    num_batches = int(np.ceil(num_samples / batch_size))
    
    for i in range(0, num_samples, batch_size):
        # Extraer el mini-batch
        x_batch = x_train_shuffled[i:i+batch_size]
        y_batch = y_train_oh_shuffled[i:i+batch_size]
        m = x_batch.shape[0] # Tamaño real del batch (el último puede ser menor)
        
        # 1. Forward
        z1 = np.dot(x_batch, W1) + b1
        a1 = relu(z1)

        z2 = np.dot(a1, W2) + b2
        a2 = softmax(z2)

        # Loss acumulada
        loss = -np.sum(y_batch * np.log(a2 + 1e-8)) / m
        epoch_loss += loss * m

        # 2. Backward
        dz2 = a2 - y_batch
        dW2 = np.dot(a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        da1 = np.dot(dz2, W2.T)
        dz1 = da1 * relu_deriv(z1)

        dW1 = np.dot(x_batch.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        # 3. Update
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2

    total_loss = epoch_loss / num_samples
    print(f"Epoch {epoch+1}/{epochs}, Loss promedio: {total_loss:.4f}")

# -----------------------
# SAVE MODEL
# -----------------------
np.savez("model.npz", W1=W1, W2=W2, b1=b1, b2=b2)
print("Modelo guardado exitosamente en model.npz")