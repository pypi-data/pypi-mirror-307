"""
Тензор представляет собой простой многомерный массив поэтому вызову тензор как массив из n-уровней
Ниже используется стандартный импорт n-мерного массива из библиотеки Numerical Python extensions
Так же представлен вариант самостоятельно написанного тензора

P.S. Далее, временно, в пакетах будет использоваться тип данных импортированный из np так как он удобнее
"""

from numpy import ndarray

import numpy as np
from typing import Any


Tensor: ndarray


class TensorSelfWritten:
    """
    Класс для представления тензора.

    Параметры:
    ----------
    data : Any
        Данные, которые будут преобразованы в тензор
    dtype : Any, optional
        Тип данных элементов тензора (например, np.int32, np.float64)
        Если None, тип будет определен автоматически
    copy : bool, optional
        Если True (по умолчанию), создается копия данных. Если False,
        данные могут быть изменены в исходном массиве
    order : str, optional
        Порядок хранения данных в памяти ('C' для хранения построчно, 'F' для хранения по столбцам).
    """

    def __init__(self, data: Any, dtype: Any = None, copy: bool = True, order: str = 'C'):
        self.data = np.array(object=data, dtype=dtype, copy=copy, order=order)
        self.shape = self.data.shape
        self.strides = self.data.strides
        self.offset = self.data.ctypes.data - self.data.__array_interface__['data'][0]

    def __repr__(self):
        """Возвращает строковое представление тензора."""
        return f"Tensor(shape={self.shape}, dtype={self.data.dtype}, data={self.data})"

    def __getitem__(self, index):
        """
        Получает элемент тензора по заданному индексу.

        Параметры:
        ----------
        index : int or tuple
            Индекс или кортеж индексов для доступа к элементам тензора.

        Возвращает:
        ----------
        Значение элемента тензора по указанному индексу.
        """
        return self.data[index]

    @property
    def sum(self):
        """Возвращает сумму всех элементов тензора."""
        return self.data.sum()
