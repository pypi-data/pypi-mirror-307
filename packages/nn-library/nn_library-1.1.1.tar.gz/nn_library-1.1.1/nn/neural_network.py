import numpy as np

## One-hot енкодинг для міток
def one_hot_encode(labels, num_classes):
    return np.eye(num_classes)[labels]

# === Функції активацій ===
# === ReLU ===
class ReLU:
    def forward(self, x):
        self.input = x
        return np.maximum(0, x)

    def backward(self, grad_output):
        relu_grad = self.input > 0
        return grad_output * relu_grad

# === Softmax ===
class Softmax:
    def forward(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.output = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return self.output

    def backward(self, grad_output):
        return grad_output


# === Функція втрат ===
class CrossEntropyLoss:
    @staticmethod
    def forward(predictions, labels):
        return -np.mean(np.sum(labels * np.log(predictions + 1e-8), axis=1))

    @staticmethod
    def backward(predictions, labels):
        return predictions - labels


# === Шар Dense ===
class DenseLayer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))

    def forward(self, x):
        self.input = x
        self.output = np.dot(x, self.weights) + self.biases
        return self.output

    def backward(self, grad_output):
        grad_input = np.dot(grad_output, self.weights.T)
        grad_weights = np.dot(self.input.T, grad_output)
        grad_biases = np.sum(grad_output, axis=0, keepdims=True)

        self.grad_weights = grad_weights
        self.grad_biases = grad_biases

        return grad_input


# === Оптимізатор SGD ===
class SGDOptimizer:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def update(self, layer):
        layer.weights -= self.learning_rate * layer.grad_weights
        layer.biases -= self.learning_rate * layer.grad_biases

# === Оптимізатор RMSProp ===
class RMSPropOptimizer:
    def __init__(self, learning_rate=0.001, beta=0.9, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta = beta
        self.epsilon = epsilon
        self.cache = {}

    def update(self, layer):
        # Оновлюємо тільки шари, які мають ваги (DenseLayer)
        if hasattr(layer, 'weights'):
            # Ініціалізація накопичувальної змінної для ваг та зміщень
            if layer not in self.cache:
                self.cache[layer] = {
                    'weight_cache': np.zeros_like(layer.weights),
                    'bias_cache': np.zeros_like(layer.biases)
                }

            # Оновлення накопичувальної змінної для ваг
            self.cache[layer]['weight_cache'] = (
                self.beta * self.cache[layer]['weight_cache'] +
                (1 - self.beta) * layer.grad_weights**2
            )
            # Оновлення ваг
            layer.weights -= self.learning_rate * layer.grad_weights / (
                np.sqrt(self.cache[layer]['weight_cache']) + self.epsilon
            )

            # Оновлення накопичувальної змінної для зміщень
            self.cache[layer]['bias_cache'] = (
                self.beta * self.cache[layer]['bias_cache'] +
                (1 - self.beta) * layer.grad_biases**2
            )
            # Оновлення зміщень
            layer.biases -= self.learning_rate * layer.grad_biases / (
                np.sqrt(self.cache[layer]['bias_cache']) + self.epsilon
            )


# === Нейронна мережа ===
class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.loss_fn = CrossEntropyLoss()
        self.optimizer = RMSPropOptimizer(learning_rate=0.001)

    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad_output):
        for layer in reversed(self.layers):
            grad_output = layer.backward(grad_output)

    def train_on_batch(self, x, y):
        # Прямий прохід
        predictions = self.forward(x)

        # Обчислення втрат
        loss = self.loss_fn.forward(predictions, y)

        # Зворотний прохід
        grad_loss = self.loss_fn.backward(predictions, y)
        self.backward(grad_loss)

        # Оновлення ваг
        for layer in self.layers:
            self.optimizer.update(layer)

        return loss

    def predict(self, x):
        predictions = self.forward(x)
        return np.argmax(predictions, axis=1)


def train(network, train_images, train_labels_one_hot, train_labels, epochs, batch_size):
    for epoch in range(epochs):
        epoch_loss = 0
        num_batches = 0
        for i in range(0, train_images.shape[0], batch_size):
            X_batch = train_images[i:i+batch_size]
            y_batch = train_labels_one_hot[i:i+batch_size]

            loss = network.train_on_batch(X_batch, y_batch)
            epoch_loss += loss
            num_batches += 1

        epoch_loss /= num_batches

        # Точність на тренувальних даних
        predictions = network.predict(train_images)
        accuracy = np.mean(predictions == train_labels)
        print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}, Accuracy: {accuracy * 100:.2f}%')
