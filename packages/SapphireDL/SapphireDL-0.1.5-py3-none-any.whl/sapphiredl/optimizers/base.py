from neural_networks import NeuralNetwork


class Optimizer:
    """
    Базовый класс для оптимизаторов
    Этот класс должен быть унаследован для реализации конкретных алгоритмов оптимизации
    """

    def step(self, nn: NeuralNetwork) -> None:
        """
        Выполняет шаг оптимизации для заданной нейронной сети

        :arg
            nn (NeuralNetwork): Нейронная сеть, для которой выполняется оптимизация.

        :raise:
            NotImplementedError: Этот метод должен быть реализован в подклассе.
        """
        raise NotImplementedError
