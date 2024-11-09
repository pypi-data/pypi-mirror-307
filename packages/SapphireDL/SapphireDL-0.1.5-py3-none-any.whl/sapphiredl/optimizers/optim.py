import numpy as np

from neural_networks import NeuralNetwork
from optimizers.base import Optimizer


# Stochastic gradient descent optimizer
# Оптимизатор стохастического градиентного спуска
class SGD(Optimizer):
    def __init__(self, lr: float = 0.01) -> None:
        """
        Инициализирует оптимизатор SGD с заданной скоростью обучения

        :param
            learning_rate (float): Скорость обучения для обновления параметров. По умолчанию 0.01
        """
        self.learning_rate = lr

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети

        :arg
            NeuralNetwork: Нейронная сеть, параметры которой будут обновлены

        Обновляет параметры сети с использованием градиентов и заданной скорости обучения
        """
        for parameter, gradient in nn.parameters_and_gradients():
            parameter -= self.learning_rate * gradient


class Momentum(Optimizer):
    """
    Оптимизатор с momentum
    Этот оптимизатор используется для ускорения градиентного спуска.
    """

    def __init__(self, lr: float = 0.01, momentum: float = 0.9) -> None:
        """
        Инициализирует оптимизатор Momentum с заданной скоростью обучения и момента

        :param lr: Скорость обучения для обновления параметров (по умолчанию 0.01).
        :param momentum: Коэффициент момента (по умолчанию 0.9).
        """
        self.learning_rate = lr
        self.momentum = momentum
        self.speeds = dict()

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети с использованием момента

        :arg nn: Нейронная сеть, параметры которой будут обновлены.
        """
        for parameter, gradient in nn.parameters_and_gradients():

            if parameter not in self.speeds:
                self.speeds[parameter] = np.zeros_like(parameter)

            self.speeds[parameter] = self.momentum * self.speeds[parameter] - self.learning_rate * gradient

            parameter += self.speeds[parameter]


class Adam(Optimizer):
    """
    Адаптивный оптимизатор Adam. Популярный оптимизатор, как и в torch, надо сделать
    Этот оптимизатор использует моменты первого и второго порядка для адаптации скорости обучения.
    """

    def __init__(self,
                 lr: float = 0.001,
                 beta1: float = 0.9,
                 beta2: float = 0.999,
                 e: float = 1e-8) -> None:
        """
        Инициализирует оптимизатор Adam с заданными параметрами.

        :param lr: Скорость обучения (по умолчанию 0.001).
        :param beta1: Коэффициент для первого момента (по умолчанию 0.9).
        :param beta2: Коэффициент для второго момента (по умолчанию 0.999).
        :param e: Значение для избежания деления на ноль (по умолчанию 1e-8).
        """
        self.learning_rate = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = e
        self.momentum = dict()
        self.speeds = dict()
        self.stc = 0

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети с использованием метода Adam.

        :arg nn: Нейронная сеть, параметры которой будут обновлены.
        """
        self.stc += 1
        for parameter, gradient in nn.parameters_and_gradients():
            if parameter not in self.momentum:
                self.momentum[parameter] = np.zeros_like(parameter)
                self.speeds[parameter] = np.zeros_like(parameter)

            # Обновление моментов
            self.momentum[parameter] = self.beta1 * self.momentum[parameter] + (1 - self.beta1) * gradient
            self.speeds[parameter] = self.beta2 * self.speeds[parameter] + (1 - self.beta2) * (gradient ** 2)

            # Коррекция смещения
            mo_h = self.momentum[parameter] / (1 - self.beta1 ** self.stc)
            sp_h = self.speeds[parameter] / (1 - self.beta2 ** self.stc)

            # Обновление параметров
            parameter -= self.learning_rate * mo_h / (np.sqrt(sp_h) + self.epsilon)


class RMSop(Optimizer):
    """
    Оптимизатор RMSop.
    Этот оптимизатор использует скользящее среднее квадратов градиентов для адаптации скорости обучения.
    """

    def __init__(self, lr: float = 0.001, dr: float = 0.99, e: float = 1e-8) -> None:
        """
        Инициализирует оптимизатор RMSop с заданными параметрами.

        :param lr: Скорость обучения (по умолчанию 0.001).
        :param dr: Коэффициент затухания для скользящего среднего квадратов градиентов (по умолчанию 0.99).
        :param e: Значение для избежания деления на ноль (по умолчанию 1e-8).
        """
        self.learning_rate = lr
        self.decay_rate = dr
        self.epsilon = e
        self.cache = dict()

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети с использованием метода RMSop.

        :arg nn: Нейронная сеть, параметры которой будут обновлены.
        """
        for parameter, gradient in nn.parameters_and_gradients():

            if parameter not in self.cache:
                self.cache[parameter] = np.zeros_like(parameter)

            # Обновление кэша
            self.cache[parameter] = (self.decay_rate * self.cache[parameter] + (1 - self.decay_rate) * (gradient ** 2))

            # Обновление параметров
            parameter -= (self.learning_rate / (np.sqrt(self.cache[parameter]) + self.epsilon)) * gradient


class NAG(Optimizer):
    """
    Оптимизатор Nester Accelerated Gradient (NAG).
    Этот оптимизатор использует momentum с предварительным шагом для улучшения сходимости.
    """

    def __init__(self, lr: float = 0.01, momentum: float = 0.9) -> None:
        """
        Инициализирует оптимизатор NAG с заданной скоростью обучения

        :param lr: Скорость обучения для обновления параметров (по умолчанию 0.01).
        :param momentum: Коэффициент (по умолчанию 0.9).
        """
        self.learning_rate = lr
        self.momentum = momentum
        self.velocities = {}

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети с использованием NAG.

        :arg nn: Нейронная сеть, параметры которой будут обновлены.
        """
        for parameter, gradient in nn.parameters_and_gradients():
            if parameter not in self.velocities:
                self.velocities[parameter] = np.zeros_like(parameter)

            # Предварительный шаг в направлении momentum
            t_param = parameter + self.momentum * self.velocities[parameter]

            # Обновление self.velocities[parameter]
            self.velocities[parameter] = self.momentum * self.velocities[parameter] - self.learning_rate * t_param

            # Обновление параметров
            parameter += self.velocities[parameter]


class AdaDelta(Optimizer):
    """
    Оптимизатор AdaDelta
    Этот оптимизатор является улучшенной версией Adam и требует меньшей настройки. Но Adam стабильнее
    """

    def __init__(self, dr: float = 0.95, e: float = 1e-6) -> None:
        """
        Инициализирует оптимизатор AdaDelta с заданными параметрами.

        :param dr: Коэффициент затухания для скользящего среднего (по умолчанию 0.95).
        :param e: Значение для избежания деления на ноль (по умолчанию 1e-6).
        """
        self.decay_rate = dr
        self.epsilon = e
        self.accumulated_gradients = dict()
        self.accumulated_updates = dict()

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг обновления параметров нейронной сети с использованием метода AdaDelta.

        :arg nn: Нейронная сеть, параметры которой будут обновлены.
        """
        for parameter, gradient in nn.parameters_and_gradients():
            if parameter not in self.accumulated_gradients:
                self.accumulated_gradients[parameter] = np.zeros_like(parameter)
                self.accumulated_updates[parameter] = np.zeros_like(parameter)

            # Обновление скользящего среднего квадратов градиентов
            self.accumulated_gradients[parameter] = (
                    self.decay_rate * self.accumulated_gradients[parameter] + (1 - self.decay_rate) * (gradient ** 2)
            )

            # Вычисление шага обновления
            update = (
                    np.sqrt(self.accumulated_updates[parameter] + self.epsilon) /
                    np.sqrt(self.accumulated_gradients[parameter] + self.epsilon) *
                    gradient
            )

            # Обновление скользящего среднего квадратов обновлений
            self.accumulated_updates[parameter] = (
                    self.decay_rate * self.accumulated_updates[parameter] + (1 - self.decay_rate) * (update ** 2)
            )

            # Обновление параметров
            parameter -= update
