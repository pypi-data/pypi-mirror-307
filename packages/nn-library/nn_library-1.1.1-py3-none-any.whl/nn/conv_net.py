import numpy as np
from scipy.signal import correlate2d
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical


class Layer:
    def forward(self, input_data):
        raise NotImplementedError

    def backward(self, gradient, learning_rate):
        raise NotImplementedError


class Conv2D(Layer):
    def __init__(self, filters, kernel_size, activation="relu"):
        self.num_filters = filters
        self.kernel_size = kernel_size
        self.activation = activation
        self.filters = None
        self.biases = None
        self.optimizer = RMSprop()

    def initialize(self, input_shape):
        input_height, input_width, input_channels = input_shape
        self.input_channels = input_channels

        # Xavier initialization for filters
        limit = np.sqrt(2.0 / (input_channels * self.kernel_size * self.kernel_size))
        self.filters = np.random.normal(0, limit,
                                      (self.num_filters, self.kernel_size,
                                       self.kernel_size, self.input_channels))

        # Calculate output dimensions
        self.output_height = input_height - self.kernel_size + 1
        self.output_width = input_width - self.kernel_size + 1
        self.biases = np.zeros((self.num_filters, 1, 1))

        return (self.output_height, self.output_width, self.num_filters)

    def forward(self, input_data):
        self.input_data = input_data
        self.batch_size = input_data.shape[0]

        output = np.zeros((self.batch_size, self.output_height, self.output_width, self.num_filters))

        for b in range(self.batch_size):
            for f in range(self.num_filters):
                conv_result = np.zeros((self.output_height, self.output_width))
                for c in range(self.input_channels):
                    conv_result += correlate2d(self.input_data[b, :, :, c],
                                            self.filters[f, :, :, c],
                                            mode="valid")
                output[b, :, :, f] = conv_result + self.biases[f]

        self.pre_activation = output

        if self.activation == "relu":
            self.output = np.maximum(0, output)

        return self.output

    def backward(self, gradient, learning_rate):
        if self.activation == "relu":
            gradient = gradient * (self.pre_activation > 0)

        dL_dinput = np.zeros_like(self.input_data)
        dL_dfilters = np.zeros_like(self.filters)
        dL_dbiases = np.zeros((self.num_filters, 1, 1))

        for b in range(self.batch_size):
            for f in range(self.num_filters):
                dL_dbiases[f] += np.sum(gradient[b, :, :, f])

                for c in range(self.input_channels):
                    dL_dfilters[f, :, :, c] += correlate2d(self.input_data[b, :, :, c],
                                                         gradient[b, :, :, f],
                                                         mode="valid")
                    dL_dinput[b, :, :, c] += correlate2d(gradient[b, :, :, f],
                                                       self.filters[f, :, :, c],
                                                       mode="full")

        # Apply gradient clipping
        clip_value = 5.0
        dL_dfilters = np.clip(dL_dfilters, -clip_value, clip_value)
        dL_dbiases = np.clip(dL_dbiases, -clip_value, clip_value)

        # Add L2 regularization
        l2_lambda = 0.01
        dL_dfilters += l2_lambda * self.filters

        # Update parameters using RMSprop
        self.filters = self.optimizer.update(self.filters, dL_dfilters, f'conv2d_filters_{id(self)}')
        self.biases = self.optimizer.update(self.biases, dL_dbiases, f'conv2d_biases_{id(self)}')

        return dL_dinput


class MaxPool2D(Layer):
    def __init__(self, pool_size):
        self.pool_size = pool_size

    def initialize(self, input_shape):
        input_height, input_width, channels = input_shape
        self.output_height = input_height // self.pool_size
        self.output_width = input_width // self.pool_size
        return (self.output_height, self.output_width, channels)

    def forward(self, input_data):
        self.input_data = input_data
        self.batch_size = input_data.shape[0]
        _, self.input_height, self.input_width, self.channels = input_data.shape

        output = np.zeros((self.batch_size, self.output_height, self.output_width, self.channels))
        self.cache = {}  # Store indices of max values

        for b in range(self.batch_size):
            for c in range(self.channels):
                for i in range(self.output_height):
                    for j in range(self.output_width):
                        start_i = i * self.pool_size
                        start_j = j * self.pool_size
                        end_i = start_i + self.pool_size
                        end_j = start_j + self.pool_size

                        patch = input_data[b, start_i:end_i, start_j:end_j, c]
                        output[b, i, j, c] = np.max(patch)
                        # Store the indices of max value
                        self.cache[(b,i,j,c)] = np.unravel_index(np.argmax(patch), patch.shape)

        return output

    def backward(self, gradient, learning_rate):
        dL_dinput = np.zeros_like(self.input_data)

        for b in range(self.batch_size):
            for c in range(self.channels):
                for i in range(self.output_height):
                    for j in range(self.output_width):
                        start_i = i * self.pool_size
                        start_j = j * self.pool_size
                        end_i = start_i + self.pool_size
                        end_j = start_j + self.pool_size

                        max_i, max_j = self.cache[(b,i,j,c)]
                        dL_dinput[b, start_i + max_i, start_j + max_j, c] = gradient[b, i, j, c]

        return dL_dinput


class Flatten(Layer):
    def initialize(self, input_shape):
        self.input_shape = input_shape
        return (np.prod(input_shape),)

    def forward(self, input_data):
        self.batch_size = input_data.shape[0]
        return input_data.reshape(self.batch_size, -1)

    def backward(self, gradient, learning_rate):
        return gradient.reshape(self.batch_size, *self.input_shape)


class RMSprop:
    def __init__(self, learning_rate=0.001, beta=0.9, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta = beta
        self.epsilon = epsilon
        self.v = {}  # Moving average of squared gradients

    def update(self, params, gradients, param_id):
        if param_id not in self.v:
            self.v[param_id] = np.zeros_like(params)

        # Update moving average of squared gradients
        self.v[param_id] = self.beta * self.v[param_id] + (1 - self.beta) * np.square(gradients)

        # Update parameters
        return params - (self.learning_rate / (np.sqrt(self.v[param_id]) + self.epsilon)) * gradients


class BatchNormalization(Layer):
    def __init__(self, epsilon=1e-8):
        self.epsilon = epsilon
        self.gamma = None
        self.beta = None
        self.optimizer_gamma = RMSprop()
        self.optimizer_beta = RMSprop()

    def initialize(self, input_shape):
        self.gamma = np.ones(input_shape)
        self.beta = np.zeros(input_shape)
        return input_shape

    def forward(self, input_data):
        self.input_data = input_data
        self.batch_size = input_data.shape[0]

        # Calculate mean and variance
        self.mean = np.mean(input_data, axis=0)
        self.variance = np.var(input_data, axis=0)

        # Normalize
        self.normalized = (input_data - self.mean) / np.sqrt(self.variance + self.epsilon)

        # Scale and shift
        return self.gamma * self.normalized + self.beta

    def backward(self, gradient, learning_rate):
        # Gradient with respect to gamma and beta
        dgamma = np.sum(gradient * self.normalized, axis=0)
        dbeta = np.sum(gradient, axis=0)

        # Update parameters using RMSprop
        self.gamma = self.optimizer_gamma.update(self.gamma, dgamma, f'bn_gamma_{id(self)}')
        self.beta = self.optimizer_beta.update(self.beta, dbeta, f'bn_beta_{id(self)}')

        # Gradient with respect to input
        return gradient * self.gamma / np.sqrt(self.variance + self.epsilon)

class Dense(Layer):
    def __init__(self, units, activation="softmax"):
        self.units = units
        self.activation = activation
        self.optimizer = RMSprop()

    def initialize(self, input_shape):
        self.input_dim = input_shape[0]
        # Xavier initialization
        limit = np.sqrt(2.0 / self.input_dim)
        self.weights = np.random.normal(0, limit, (self.input_dim, self.units))
        self.biases = np.zeros((1, self.units))
        return (self.units,)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, input_data):
        self.input_data = input_data
        self.z = np.dot(input_data, self.weights) + self.biases

        if self.activation == "softmax":
            self.output = self.softmax(self.z)
        elif self.activation == "relu":
            self.output = np.maximum(0, self.z)

        return self.output

    def backward(self, gradient, learning_rate):
        if self.activation == "softmax":
            dL_dz = gradient
        elif self.activation == "relu":
            dL_dz = gradient * (self.z > 0)

        dL_dw = np.dot(self.input_data.T, dL_dz)
        dL_db = np.sum(dL_dz, axis=0, keepdims=True)
        dL_dinput = np.dot(dL_dz, self.weights.T)

        # Gradient clipping
        clip_value = 5.0
        dL_dw = np.clip(dL_dw, -clip_value, clip_value)
        dL_db = np.clip(dL_db, -clip_value, clip_value)

        # L2 regularization
        l2_lambda = 0.01
        dL_dw += l2_lambda * self.weights

        # Update parameters using RMSprop
        self.weights = self.optimizer.update(self.weights, dL_dw, f'dense_weights_{id(self)}')
        self.biases = self.optimizer.update(self.biases, dL_db, f'dense_biases_{id(self)}')

        return dL_dinput


class CNN:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def initialize(self, input_shape):
        current_shape = input_shape
        for layer in self.layers:
            current_shape = layer.initialize(current_shape)

    def forward(self, X):
        current_output = X
        for layer in self.layers:
            current_output = layer.forward(current_output)
        return current_output

    def backward(self, gradient, learning_rate):
        current_gradient = gradient
        for layer in reversed(self.layers):
            current_gradient = layer.backward(current_gradient, learning_rate)

    def train(self, X_train, y_train, epochs=5, batch_size=128, learning_rate=0.001):
        num_samples = X_train.shape[0]
        best_accuracy = 0
        patience = 5
        patience_counter = 0

        for epoch in range(epochs):
            print(f"Epoch {epoch + 1}/{epochs}")

            # Learning rate decay
            current_lr = learning_rate * (0.95 ** epoch)

            # Shuffle the training data
            indices = np.random.permutation(num_samples)
            X_train = X_train[indices]
            y_train = y_train[indices]

            total_loss = 0
            correct_predictions = 0
            num_batches = num_samples // batch_size

            for batch_idx in range(num_batches):
                start_idx = batch_idx * batch_size
                end_idx = start_idx + batch_size

                X_batch = X_train[start_idx:end_idx]
                y_batch = y_train[start_idx:end_idx]

                # Add noise to input (data augmentation)
                if np.random.random() < 0.5:
                    X_batch = X_batch + np.random.normal(0, 0.01, X_batch.shape)
                    X_batch = np.clip(X_batch, 0, 1)

                # Forward pass
                predictions = self.forward(X_batch)

                # Calculate accuracy
                predicted_classes = np.argmax(predictions, axis=1)
                true_classes = np.argmax(y_batch, axis=1)
                batch_correct = np.sum(predicted_classes == true_classes)
                correct_predictions += batch_correct

                # Calculate loss
                loss = -np.mean(np.sum(y_batch * np.log(predictions + 1e-7), axis=1))
                total_loss += loss

                # Backward pass
                gradient = (predictions - y_batch) / batch_size
                self.backward(gradient, current_lr)

                if batch_idx % 10 == 0:
                    batch_accuracy = batch_correct / batch_size * 100
                    print(f"Batch {batch_idx}/{num_batches} - Loss: {loss:.4f} - Accuracy: {batch_accuracy:.2f}%")

            # Calculate epoch statistics
            avg_loss = total_loss / num_batches
            accuracy = correct_predictions / num_samples * 100

            print(f"Epoch {epoch + 1}/{epochs} - Average Loss: {avg_loss:.4f} - Accuracy: {accuracy:.2f}%")

            # Early stopping
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                print("Early stopping triggered")
                break


def load_mnist_data():
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    train_images = train_images.reshape(60000, 28, 28, 1)
    train_images = train_images.astype("float32") / 255

    test_images = test_images.reshape(10000, 28, 28, 1)
    test_images = test_images.astype("float32") / 255

    # Convert labels to one-hot encoding
    train_labels = to_categorical(train_labels, 10)
    test_labels = to_categorical(test_labels, 10)

    return train_images, train_labels, test_images, test_labels

def evaluate_model(model, X_test, y_test, batch_size=128):
    num_samples = X_test.shape[0]
    num_batches = num_samples // batch_size
    correct_predictions = 0
    total_loss = 0
    all_predictions = []

    print("Evaluating model on test set...")

    for batch_idx in range(num_batches):
        start_idx = batch_idx * batch_size
        end_idx = start_idx + batch_size

        X_batch = X_test[start_idx:end_idx]
        y_batch = y_test[start_idx:end_idx]

        # Forward pass
        predictions = model.forward(X_batch)
        all_predictions.extend(predictions)

        # Calculate accuracy
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y_batch, axis=1)
        batch_correct = np.sum(predicted_classes == true_classes)
        correct_predictions += batch_correct

        # Calculate loss
        loss = -np.mean(np.sum(y_batch * np.log(predictions + 1e-7), axis=1))
        total_loss += loss

        if batch_idx % 10 == 0:
            batch_accuracy = batch_correct / batch_size * 100
            print(f"Batch {batch_idx}/{num_batches} - Loss: {loss:.4f} - Accuracy: {batch_accuracy:.2f}%")

    # Handle remaining samples
    if num_samples % batch_size != 0:
        start_idx = num_batches * batch_size
        X_batch = X_test[start_idx:]
        y_batch = y_test[start_idx:]

        predictions = model.forward(X_batch)
        all_predictions.extend(predictions)

        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y_batch, axis=1)
        correct_predictions += np.sum(predicted_classes == true_classes)

    # Calculate final metrics
    avg_loss = total_loss / num_batches
    accuracy = correct_predictions / num_samples * 100

    print(f"\nTest Set Evaluation:")
    print(f"Average Loss: {avg_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")

    return np.array(all_predictions)


