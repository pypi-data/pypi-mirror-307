import numpy as np

from typing import Callable, List, Any

from numpy import dtype, floating
from numpy._typing import _64Bit, _128Bit
from numpy.typing import NBitBase

from layers.meaning.base import BaseLayer
from tensors import Tensor


F: Callable[[Tensor], Tensor]


class LinearLayer(BaseLayer):
    def __init__(self, input_size: int, output_size: int) -> None:
        """
        Инициализация линейного слоя

        :argument input_size (int): Размер входных данных
        :argument output_size (int): Размер выходных данных

        Инициализация весов и смещений
        """
        super().__init__()
        self.parameters['weights'] = np.random.rand(input_size, output_size)
        self.parameters['bias'] = np.random.rand(output_size)

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение через линейный слой

        :return Tensor: Выходные данные после применения линейного преобразования

        Сохраняет входные данные для использования в обратном распространении
        """
        self.inputs = inputs
        return inputs @ self.parameters['weights'] + self.parameters['bias']

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение через линейный слой.

        :return Tensor: Градиент для предыдущего слоя.

        Вычисляет градиенты для весов и смещений и возвращает градиент для предыдущего слоя.
        """
        self.gradients['bias'] = np.sum(gradient, axis=0)
        self.gradients['weights'] = self.inputs.T @ gradient
        return gradient @ self.parameters['weights'].T


class Sequential:
    def __init__(self) -> None:
        """
        Инициализация последовательной модели.

        Создает пустой список для хранения слоев.
        """
        self.layers: List[Callable] = list()

    def add(self, layer: Callable) -> None:
        """
        Добавление слоя в последовательную модель.

        :argument layer: Слой, который будет добавлен в модель.
        """
        self.layers.append(layer)

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение через все слои модели.

        :return Tensor: Выходные данные после применения всех слоев.
        """
        for layer in self.layers:
            inputs = layer.forward(inputs)

        return inputs

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение через все слои модели.

        :return Tensor: Градиент для предыдущего слоя.
        """
        for layer in reversed(self.layers):
            gradient = layer.backward(gradient)

        return gradient

    def zero_grad(self) -> None:
        """
        Обнуление градиентов всех слоев.

        Используется перед обновлением весов.
        """
        for layer in self.layers:
            layer.zero_grad()


class RecurrentLayer(BaseLayer):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        """
        Инициализация рекуррентного слоя

        :argument input_size (int): Размер входных данных
        :argument hidden_size (int): Размер скрытого состояния

        Инициализация весов и смещений
        """
        super().__init__()
        self.hidden_states = None
        self.parameters['weights_input'] = np.random.rand(input_size, hidden_size)
        self.parameters['weights_hidden'] = np.random.rand(hidden_size, hidden_size)
        self.parameters['bias'] = np.zeros((1, hidden_size))

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение через рекуррентный слой

        :return Tensor: Выходные данные после применения рекуррентного преобразования

        Сохраняет входные данные для использования в обратном распространении
        """
        self.inputs = inputs
        self.hidden_states = np.zeros((inputs.shape[0], inputs.shape[1],
                                       self.parameters['weights_hidden'].shape[1]))

        for t in range(inputs.shape[1]):
            if t == 0:
                self.hidden_states[:, t, :] = np.tanh(np.dot(inputs[:, t, :],
                                                             self.parameters['weights_input']) + self.parameters['bias']
                                                      )
            else:
                self.hidden_states[:, t, :] = np.tanh(np.dot(inputs[:, t, :], self.parameters['weights_input']) +
                                                      np.dot(self.hidden_states[:, t - 1, :],
                                                             self.parameters['weights_hidden']) +
                                                      self.parameters['bias'])

        return self.hidden_states

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение через рекуррентный слой.

        :return Tensor: Градиент для предыдущего слоя.

        Вычисляет градиенты для весов и смещений и возвращает градиент для предыдущего слоя.
        """
        self.gradients['bias'] = np.sum(gradient, axis=(0, 1))

        grad_weights_input = np.zeros_like(self.parameters['weights_input'])
        grad_weights_hidden = np.zeros_like(self.parameters['weights_hidden'])

        for t in reversed(range(gradient.shape[1])):
            if t == gradient.shape[1] - 1:
                grad_weights_input += (
                        self.inputs[:, t, :].T @
                        (gradient[:, t, :] *
                         (1 - np.tanh(self.hidden_states[:, t, :]) ** 2)))
                grad_weights_hidden += (
                        self.hidden_states[:, t - 1, :].T @
                        (gradient[:, t, :] *
                         (1 - np.tanh(self.hidden_states[:, t, :]) ** 2)))
            else:
                grad_weights_input += (
                        self.inputs[:, t, :].T @
                        (gradient[:, t, :] *
                         (1 - np.tanh(self.hidden_states[:, t, :]) ** 2) +
                         gradient[:, t + 1, :] *
                         (1 - np.tanh(self.hidden_states[:, t + 1, :]) ** 2)))
                grad_weights_hidden += (
                        self.hidden_states[:, t - 1, :].T @
                        (gradient[:, t, :] *
                         (1 - np.tanh(self.hidden_states[:, t, :]) ** 2) +
                         gradient[:, t + 1, :] *
                         (1 - np.tanh(self.hidden_states[:, t + 1, :]) ** 2)))

        return self.hidden_states[:, :-1, :]


class PoolingLayer(BaseLayer):
    def __init__(self, pool_size: int) -> None:
        """
        Инициализация пул слоя

        :argument pool_size (int): Размер пула
        """
        super().__init__()
        self.pooled_output = None
        self.output_width = None
        self.output_height = None
        self.pool_size = pool_size

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение через пул слой

        :return Tensor: Выходные данные после применения пула

        Сохраняет входные данные для использования в обратном распространении
        """
        self.inputs = inputs
        self.output_height = inputs.shape[1] // self.pool_size
        self.output_width = inputs.shape[2] // self.pool_size

        self.pooled_output = np.zeros(
            (
                inputs.shape[0],
                self.output_height,
                self.output_width,
                inputs.shape[3]
            )
        )

        for n in range(inputs.shape[0]):
            for c in range(inputs.shape[3]):
                for i in range(self.output_height):
                    for j in range(self.output_width):
                        self.pooled_output[n, i, j, c] = (
                            np.max(
                                inputs[
                                n,
                                i * self.pool_size: (i + 1) * self.pool_size,
                                j * self.pool_size: (j + 1) * self.pool_size,
                                c
                                ]
                            )
                        )

        return self.pooled_output

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение через пул слой.

        :return Tensor: Градиент для предыдущего слоя.

        Вычисляет градиенты и возвращает градиент для предыдущего слоя.
        """
        grad_input = np.zeros_like(self.inputs)

        for n in range(gradient.shape[0]):
            for c in range(gradient.shape[3]):
                for i in range(gradient.shape[1]):
                    for j in range(gradient.shape[2]):
                        max_index = np.unravel_index(
                            np.argmax(
                                self.inputs[
                                n,
                                i * self.pool_size: (i + 1) * self.pool_size,
                                j * self.pool_size: (j + 1) * self.pool_size,
                                c
                                ]
                            ),
                            (self.pool_size, self.pool_size)
                        )
                        grad_input[
                            n,
                            i * self.pool_size + max_index[0],
                            j * self.pool_size + max_index[1], c
                        ] = gradient[n, i, j, c]

        return grad_input


class ConvolutionalLayer(BaseLayer):
    convolved_outputs: (Tensor[Any, dtype[floating[_64Bit]]] |
                        Tensor[Any, dtype[floating[_128Bit]]] |
                        Tensor[Any, dtype[floating[NBitBase]]])

    def __init__(
            self,
            input_channels: int,
            output_channels: int,
            kernel_size: int,
            stride: int) -> None:
        """
        Инициализация слоя свёртки

        :argument input_channels (int): Количество входных каналов
        :argument output_channels (int): Количество выходных каналов
        :argument kernel_size (int): Размер ядра свертки
        :argument stride (int): Шаг свертки
        """

        super().__init__()
        self.input_channels = input_channels
        self.output_channels = output_channels
        self.kernel_size = kernel_size
        self.stride = stride

        self.parameters['weights'] = np.random.rand(
            output_channels,
            input_channels,
            kernel_size,
            kernel_size
        )
        self.parameters['bias'] = np.zeros((1, output_channels))

    def forward_conv(self, inputs: Tensor, outputs_channels: int) -> Tensor:
        """
        Прямое распространение через слой свёртки

        :return Tensor: Выходные данные после применения свертки

        Сохраняет входные данные для использования в обратном распространении
        """
        self.inputs = inputs
        input_height, input_width = inputs.shape[1], inputs.shape[2]
        output_height = (input_height - self.kernel_size) // self.stride + 1
        output_width = (input_width - self.kernel_size) // self.stride + 1

        self.convolved_outputs = np.zeros((inputs.shape[0], output_height, output_width, outputs_channels))

        for n in range(inputs.shape[0]):
            for c_out in range(self.output_channels):
                for i in range(output_height):
                    for j in range(output_width):
                        self.convolved_outputs[
                            n,
                            i,
                            j,
                            c_out
                        ] = np.sum(
                            inputs[
                            n,
                            i * self.stride: i * self.stride + self.kernel_size,
                            j * self.stride: j * self.stride + self.kernel_size:
                            ] * self.parameters['weights'][c_out, :, :, :]) + self.parameters['bias'][0, c_out]

        return self.convolved_outputs

    def backward_conv(self, gradient: Tensor) -> tuple[Tensor, Tensor, Any] | list[Tensor, Tensor, Any]:
        """
        Обратное распространение через слой свёртки

        :return Tensor: Градиент для предыдущего слоя.

        Вычисляет градиенты и возвращает градиент для предыдущего слоя.
        """
        grad_input = np.zeros_like(self.inputs)
        grad_weights = np.zeros_like(self.parameters['weights'])
        grad_bias = np.sum(gradient, axis=(0, 1, 2))

        for n in range(gradient.shape[0]):
            for c_out in range(self.output_channels):
                for i in range(gradient.shape[1]):
                    for j in range(gradient.shape[2]):
                        grad_input[
                        n,
                        i * self.stride: i * self.stride + self.kernel_size,
                        j * self.stride:j * self.stride + self.kernel_size,
                        :
                        ] += (
                                gradient[n, i, j, c_out] * self.parameters['weights'][c_out, :, :, :]
                        )
                        grad_weights[c_out, :, :, :] += (
                                gradient[
                                    n,
                                    i,
                                    j,
                                    c_out
                                ] * self.inputs[
                                    n,
                                    i * self.stride:i * self.stride + self.kernel_size,
                                    j * self.stride:j * self.stride + self.kernel_size,
                                    :
                                    ]
                        )

        return grad_input, grad_weights, grad_bias
