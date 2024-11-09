import numpy as np

from training import train
from neural_networks import NeuralNetwork
from layers import LinearLayer, HypTan

inputs = np.array([
    [0, 0],
    [1, 0],
    [0, 1],
    [1, 1]
])

targets = np.array([
    [1, 0],
    [0, 1],
    [0, 1],
    [1, 0]
])

nn = NeuralNetwork([
    LinearLayer(input_size=2, output_size=2),
    HypTan(),
    LinearLayer(input_size=2, output_size=2)
])

num_epochs = 5000

train(neural_network=nn, inputs=inputs, targets=targets, epochs_count=num_epochs)

for x, y in zip(inputs, targets):
    predicted = nn.forward(x)
    print(x, predicted, y)  # np.round(predicted, decimals=7)
