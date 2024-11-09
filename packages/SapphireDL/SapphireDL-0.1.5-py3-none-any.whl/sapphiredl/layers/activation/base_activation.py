from tensors import Tensor
from layers.meaning.base import BaseLayer
from layers.meaning.layers_of_meaning import F


class ActivationLayer(BaseLayer):
    def __init__(self, function: F, function_derivative: F) -> None:
        """
        Инициализация слоя активации

        :param function (F): Функция активации
        :param function derivative (F): Производная функции активации

        Сохраняет функции активации и их производные для использования в прямом и обратном распространении
        """
        super().__init__()
        self.function = function
        self.derivative_func = function_derivative

    def forward(self, inputs: Tensor) -> Tensor:
        self.inputs = inputs
        return self.function(inputs)

    def backward(self, gradient: Tensor) -> Tensor:
        return self.derivative_func(self.inputs) * gradient
