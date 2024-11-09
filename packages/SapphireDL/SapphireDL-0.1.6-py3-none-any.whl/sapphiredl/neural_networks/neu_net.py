from sapphiredl.tensors import Tensor
from sapphiredl.layers import BaseLayer
from typing import Sequence, Iterator, Tuple


class NeuralNetwork:
    """
    Класс для представления нейронной сети
    """

    def __init__(self, layers: Sequence[BaseLayer]) -> None:
        """
        Инициализирует нейронную сеть с заданными слоями

        :argument
            layers (Sequence[BaseLayer]): Список слоев, из которых состоит нейронная сеть
        """
        self.layers = layers

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение (forward pass) через слои сети

        :argument
            inputs (Tensor): Входные данные для нейронной сети

        :return
            Tensor: Выходные данные после прохождения через все слои
        """
        for layer in self.layers:
            inputs = layer.forward(inputs)

        return inputs

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение (backward pass) градиентов через слои сети

        :argument
            gradient (Tensor): Градиенты, которые нужно распространить назад

        :return
            Tensor: Обновленные градиенты после прохождения через все слои
        """
        # self.layers / reversed(self.layers)
        for layer in reversed(self.layers):
            gradient = layer.backward(gradient)

        return gradient

    def parameters_and_gradients(self) -> Iterator[Tuple[Tensor, Tensor]]:
        """
        Генерирует пары параметров и их градиентов для всех слоев сети

        :return
            Iterator[Tuple[Tensor, Tensor]]: Итератор пар (параметр, градиент)
        """
        for layer in self.layers:

            for name, parameter in layer.parameters.items():

                gradient = layer.gradients[name]

                yield parameter, gradient

    def calculate_variable_gradient(self, t_param: Tensor) -> Tensor:
        """
        Вычисляет градиент на основе временных параметров.

        :argument
            t_param (Tensor): Временные параметры для вычисления градиента.

        :return
            Tensor: Вычисленный градиент.

        Примечание:
            Пусть реализация будет в зависимости от конкретной архитектуры нейронной сети.
            Например, метод прямого распространения и функция потерь для вычисления градиента.

        :var Тут должна быть логика для вычисления градиента на основе временных параметров.

        Абстрактный пример для логики отличной от предложенной ниже:
        outputs = self.forward(t_param)
        loss = loss_function(outputs, targets)
        grad = calculate_variable_gradient(loss)

        Выполняется прямое распространение с новыми параметрами, затем вычисление функции потерь и её производную.
        """

        raise NotImplementedError()
