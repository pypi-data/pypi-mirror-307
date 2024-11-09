import numpy as np

from tensors import Tensor
from loss_functions.base import LossType


# Mean absolute percentage error
class MAPELoss(LossType):
    def loss(self, predicted: Tensor, real: Tensor) -> float:
        # Избегание деления на ноль
        non_zero_real = real[real != 0]
        return np.mean(np.abs((non_zero_real - predicted[real != 0]) / non_zero_real)) * 100

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        # Избегание деления на ноль
        non_zero_real = real[real != 0]
        gradient = np.where(non_zero_real != 0, -100 * (real - predicted) / (non_zero_real ** 2) / len(real), 0)
        return gradient


# Symmetric mean absolute percentage error
class SMAPELoss(LossType):
    """
    Класс для вычисления потерь на основе симметричной средней абсолютной процентной ошибки
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        # Избегание деления на ноль
        denominator = np.abs(real) + np.abs(predicted)
        # Избегание деления на ноль, используя where
        return np.mean(np.where(denominator != 0, np.abs(real - predicted) / denominator, 0)) * 100

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        denominator = np.abs(real) + np.abs(predicted)
        # Избегание деления на ноль
        grad = np.where(denominator != 0, -100 * (real - predicted) / (denominator ** 2), 0)

        return grad / len(real)


# Weighted average percentage error
class WAPELoss(LossType):
    """
    Класс для вычисления потерь на основе взвешенной средней процентной ошибки
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        # Сумматор абсолютных значений реальных данных для вычисления веса
        total_real = np.sum(np.abs(real))

        # Избегание деления на ноль
        if total_real == 0:
            return float('inf')  # Или можно вернуть 0, в зависимости от контекста

        return np.sum(np.abs(real - predicted)) / total_real * 100

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        total_real = np.sum(np.abs(real))

        # Избегаем деления на ноль
        if total_real == 0:
            return np.zeros_like(predicted)  # Градиент равен нулю, если нет реальных данных

        gradient = np.sign(real - predicted) / total_real
        return gradient


class RMSLELoss(LossType):
    """
    Альтернативный способ уйти от абсолютных ошибок к относительным
        с метрикой арифметического корня среднеквадратической логарифмической ошибки
    """

    def loss(self, predicted: Tensor, real: Tensor) -> float:
        # Применение логарифма к предсказанным и реальным значениям
        log_predicted = np.log(1 + predicted)
        log_real = np.log(1 + predicted)

        # Вычисление средней квадратичной ошибки логарифмов
        mse_log = np.mean((log_predicted - log_real) ** 2)

        # Корень из MSE логарифмов на возврате
        return np.sqrt(mse_log)

    def grad(self, predicted: Tensor, real: Tensor) -> Tensor:
        # Применение логарифма к предсказанным и реальным значениям
        log_predicted = np.log(1 + predicted)
        log_real = np.log(1 + predicted)

        # Вычисление градиента
        gradient = (log_predicted - log_real) / (predicted + 1e-10)
        # + малое значение для предотвращения деления на ноль

        # Нормализованный градиент
        return gradient / len(real)
