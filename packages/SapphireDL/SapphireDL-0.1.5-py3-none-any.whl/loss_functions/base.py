from tensors import Tensor


class LossType:
    """
    Базовый класс для функции потерь

    Этот класс определяет интерфейс для функций потерь и обеспечивает
    упрощенное наследование другим классам. Он содержит методы для
    вычисления значения потерь и градиента

    Потеря - это некое нецелое число, представляющее ошибку прогноза
    Градиент - это векторная матрица ошибок
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        """
        Вычисляет значение функции потерь

        :param predicted: Прогнозируемые значения
        :param real: Реальные значения

        :return: Градиент потерь
        :raise: Если метод не реализован в подклассе
        """
        raise NotImplementedError

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        """
        Вычисляет градиент потерь

        :param predicted: Прогнозируемые значения
        :param real: Реальные значения

        :return: Градиент потерь
        :raise: Если метод не реализован в подклассе
        """
        raise NotImplementedError
