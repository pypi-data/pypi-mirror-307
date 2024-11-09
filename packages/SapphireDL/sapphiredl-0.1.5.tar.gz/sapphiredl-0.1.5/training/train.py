from tensors import Tensor
from neural_networks import NeuralNetwork
from loss_functions import MSELoss
from loss_functions.base import LossType
from optimizers import Optimizer, SGD
from data import DataIterator, BatchIterator


def train(neural_network: NeuralNetwork,
          inputs: Tensor,
          targets: Tensor,
          epochs_count: int = 1,
          iterator: DataIterator = BatchIterator(),
          loss_func: LossType = MSELoss(),
          optimizer: Optimizer = SGD()) -> None:
    """
    Обучает нейронную сеть на заданных входных данных и целевых значениях.

    Параметры:
    ----------
    neural_network : NeuralNetwork
        Нейронная сеть, которую необходимо обучить
    inputs : Tensor
        Входные данные для обучения, представленные в виде тензора
    targets : Tensor
        Целевые значения для обучения, представленные в виде тензора
    epochs_count : int, optional
        Количество эпох обучения (по умолчанию 1)
    iterator : DataIterator, optional
        Итератор для генерации batch данных (по умолчанию BatchIterator)
    loss_func : LossType, optional
        Функция потерь, используемая для вычисления ошибки (по умолчанию MSELossType)
    optimizer : Optimizer, optional
        Оптимизатор для обновления весов нейронной сети (по умолчанию SGD)

    Возвращает:
    ----------
    None
        Функция не возвращает значения, но выводит информацию о ходе обучения.

    Примечания:
    ----------
    В процессе каждой эпохи функция выводит номер эпохи и общую потерю за эту эпоху.
    """
    for epochs in range(epochs_count):
        epochs_loss = float(0)

        for batch in iterator(inputs, targets):

            predicted = neural_network.forward(inputs=batch.inputs)
            epochs_loss += loss_func.loss(predicted=predicted, real=batch.targets)
            grad = loss_func.grad(predicted=predicted, real=batch.targets)

            neural_network.backward(grad)
            optimizer.step(neural_network)

        print(epochs, epochs_loss)
