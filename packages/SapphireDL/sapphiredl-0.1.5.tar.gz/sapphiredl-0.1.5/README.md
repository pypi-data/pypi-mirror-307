# Description of the Deep Learning Library Sapphire

## Introduction
This documentation is dedicated to a deep learning library designed for the efficient creation and training of machine learning models.

## Installation
To install the library, run the following command:
```bash
pip install SapphireDL
```

## Key Features
Example for XOR

### 1. Creating a Model
The library allows you to easily create complex neural networks using high-level APIs.

```python
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
```

### 2. Training the Model
Training models becomes simple with built-in methods.

```python
num_epochs = 5000

train(neural_network=nn, inputs=inputs, targets=targets, epochs_count=num_epochs)
```

### 3. Prediction
After training, you can use the model to predict new data.

```python
for x, y in zip(inputs, targets):
    predicted = nn.forward(x)
    print(x, predicted, y)  # np.round(predicted, decimals=7)
```

## API Documentation
For more detailed information about each method and class in the library, please refer to the API documentation.

## Additional Resources

- [Documentation](https://github.com/itbert/SapphireDL/documentation)
- [Usage Examples](https://github.com/itbert/SapphireDL)
