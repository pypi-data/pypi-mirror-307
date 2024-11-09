from typing import Dict
from tensors import Tensor


class BaseLayer:
    def __init__(self) -> None:
        """
        Инициализация базового слоя

        Создает словари для хранения параметров, градиентов и входных данных
        """
        self.parameters: Dict[str, Tensor] = dict()
        self.gradients: Dict[str, Tensor] = dict()
        self.inputs: Dict = dict()

    def forward(self, inputs: Tensor) -> Tensor:
        """
        Прямое распространение (forward pass)

        :return Tensor: Выходные данные после применения слоя
        :raise NotImplementedError: Если метод не реализован в подклассе
        """
        raise NotImplementedError

    def backward(self, gradient: Tensor) -> Tensor:
        """
        Обратное распространение (backward pass)

        :return Tensor: Выходные данные после применения слоя
        :raise NotImplementedError: Если метод не реализован в подклассе
        """
        raise NotImplementedError
