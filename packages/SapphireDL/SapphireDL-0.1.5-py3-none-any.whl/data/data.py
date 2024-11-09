import numpy as np
from tensors import Tensor
from typing import Iterator, NamedTuple

# Определяем именованный кортеж для хранения пакета входных данных и целевых значений
Batch = NamedTuple("Batch", [("inputs", Tensor), ("targets", Tensor)])


class DataIterator:
    """
    Базовый класс для итераторов данных

    Этот класс должен быть унаследован для реализации конкретной логики итерации данных
    """

    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator:
        """
        Итерация по предоставленным входным данным и целевым значениям

        :argument inputs (Tensor): Входные данные
        :argument targets (Tensor): Целевые данные

        :raise NotImplementedError: Этот метод должен быть реализован в подклассе
        """
        raise NotImplementedError


class BatchIterator(DataIterator):
    """
    Итератор, который возвращает пакеты входных и целевых тензоров

    :arg batch_size (int): Размер каждого пакета
    :arg shuffle (bool): Указывает, нужно ли перемешивать данные перед пакетированием
    """

    def __init__(self, batch_size: int = 64, shuffle: bool = False):
        """
        Инициализирует BatchIterator с указанными параметрами

        :arg batch_size (int): Количество образцов в каждом пакете. По умолчанию пусть 64, как в Minecraft
        :arg shuffle (bool): Если True, перемешивает данные перед созданием пакетов. По умолчанию False
        """
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __call__(self, inputs: Tensor, targets: Tensor) -> Iterator[Batch]:
        """
        Генерирует пакеты входных и целевых тензоров

        :arg:
            inputs (Tensor): Входные данные
            targets (Tensor): Целевые данные

        :return:
            Batch: Именованный кортеж, содержащий пакет входных и целевых данных

        Пример:
            >> iterator = BatchIterator(batch_size=16, shuffle=True)
            >> for batch in iterator(inputs_tensor, targets_tensor):
                    process(batch.inputs, batch.targets)
        """
        starts = np.arange(start=0, stop=len(inputs), step=self.batch_size)

        if self.shuffle:
            np.random.shuffle(starts)

        for begin in starts:
            end = begin + self.batch_size
            batch_inputs = inputs[begin:end]
            batch_targets = targets[begin:end]
            yield Batch(batch_inputs, batch_targets)
