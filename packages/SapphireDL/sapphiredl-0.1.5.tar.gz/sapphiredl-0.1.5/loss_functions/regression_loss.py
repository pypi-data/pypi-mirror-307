import numpy as np

from tensors import Tensor
from loss_functions.base import LossType


# Mean squares error
class MSELoss(LossType):
    """
    Класс для вычисления среднеквадратичной ошибки (Mean squared error loss_func)

    Этот класс наследует от базового класса LossType и реализует методы
    для вычисления значения функции потерь и её градиента для 
    среднеквадратичной ошибки
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        return np.sum((predicted - real) ** 2)

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        return (predicted - real) * 2


# Root mean squared deviation
class RMSDLoss(LossType):
    """
    Класс для вычисления потерь на основе среднеквадратичного отклонения (RMSD)
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        return 0.5 ** ((np.sum(real - predicted) ** 2) / len(real))

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        return -((real - predicted) / len(real)) / np.sqrt(np.mean((real - predicted) ** 2))


# Mean absolute error
class MAELoss(LossType):
    """
    Класс для вычисления потерь на основе средней абсолютной ошибки (MAE)
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        return np.sum(abs(predicted - real))

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        return abs(predicted - real)


# Coefficient of determination
class R2Loss(LossType):
    """
    Класс для вычисления потерь на основе коэффициента детерминации (R²).
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        residual_sum_squares = np.sum((real - predicted) ** 2)
        total_sum_squares = np.sum((real - np.mean(real)) ** 2)

        r2 = 1 - (residual_sum_squares / total_sum_squares) if total_sum_squares != 0 else 0

        return 1 - r2

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        residual_sum_squares = np.sum((real - predicted) ** 2)
        total_sum_squares = np.sum((real - np.mean(real)) ** 2)

        if total_sum_squares == 0:
            return np.zeros_like(predicted)

        gradient = (-2 * (real - predicted)) / len(real) / (total_sum_squares / len(real))

        return gradient

