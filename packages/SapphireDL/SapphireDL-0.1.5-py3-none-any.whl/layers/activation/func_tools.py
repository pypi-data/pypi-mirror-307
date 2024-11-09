import numpy as np

from tensors import Tensor


# Гиперболический тангенс с выводом в тензор
def hyp_tan(x: Tensor) -> Tensor:
    return np.tanh(x)


# Производная гиперболического тангенса с выводом в тензор
def hyp_tan_derivative(x: Tensor) -> Tensor:
    y = hyp_tan(x)
    return 1 - y ** 2


# sigmoid функция
def sigmoid(x: Tensor) -> Tensor:
    return 1 / (1 + np.exp(-x))


# Производная sigmoid функции
def sigmoid_derivative(x: Tensor) -> Tensor:
    y = sigmoid(x)
    return y * (1 - y)


# Функция Rectified Linear Unit
def relu(x: Tensor) -> Tensor:
    return np.maximum(0, x)


# Производная Rectified Linear Unit
def relu_derivative(x: Tensor) -> Tensor:
    return np.where(x > 0, 1, 0)


# Функция Leaky Rectified Linear Unit
def leaky_relu(x: Tensor, alpha: float = 0.01) -> Tensor:
    return np.where(x > 0, x, alpha * x)


# Производная Leaky Rectified Linear Unit
def leaky_relu_derivative(x: Tensor, alpha: float = 0.01) -> Tensor:
    return np.where(x > 0, 1, alpha)


# Функция Exponential Linear Unit
def elu(x: Tensor, alpha: float = 1.0) -> Tensor:
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))


# Производная Exponential Linear Unit
def elu_derivative(x: Tensor, alpha: float = 1.0) -> Tensor:
    return np.where(x > 0, 1, elu(x) + alpha)


# Функция Softmax
def softmax(x: Tensor) -> Tensor:
    exponent_x = np.exp(x - np.max(x))  # Вычитаем max для стабильности вычислений
    return exponent_x / exponent_x.sum(axis=0)


# Производная Softmax (для много классовой классификации)
def softmax_derivative(x: Tensor) -> Tensor:
    s = softmax(x)
    return s * (1 - s)  # Для вычисления градиента необходимо использовать с учетом классов


# Gaussian Error Linear Unit (GELU)
def gelu(x: Tensor) -> Tensor:
    return 0.5 * x * (1 + hyp_tan(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


# Производная GELU
def gelu_derivative(x: Tensor) -> Tensor:
    return gelu(x) + 0.5 * (1 + hyp_tan(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


# Swish
def swish(x: Tensor) -> Tensor:
    return x * sigmoid(x)


# Производная Swish
def swish_derivative(x: Tensor) -> Tensor:
    sg = sigmoid(x)
    return sg + x * sg * (1 - sg)


# Scaled Exponential Linear Unit
def se_lu(x: Tensor) -> Tensor:
    return np.where(x > 0, 1.0507 * x, 1.0507 * (np.exp(x) - 1))


# Производная
def se_lu_derivative(x: Tensor) -> Tensor:
    return np.where(x > 0, 1.0507, 1.0507 * np.exp(x))


# M i s h
def mi_sh(x: Tensor) -> Tensor:
    return x * hyp_tan(soft_plus(x))


# Производная M i s h
def mi_sh_derivative(x: Tensor) -> Tensor:
    hyp_tan_soft_plus = hyp_tan(soft_plus(x))
    return hyp_tan_soft_plus + x * (1 - hyp_tan_soft_plus ** 2) * (1 / (1 + np.exp(-x)))


# Soft plus
def soft_plus(x: Tensor) -> Tensor:
    return np.log(1 + np.exp(x))


# Производная Soft plus
def soft_plus_derivative(x: Tensor) -> Tensor:
    return sigmoid(x)


# Hard swish
def hard_swish(x: Tensor) -> Tensor:
    return x * np.clip((x + 3) / 6, 0, 1)


# Производная Hard swish
def hard_swish_derivative(x: Tensor) -> Tensor:
    return np.where((x < -3), 0,
                    np.where((x > 3), 1,
                             (x + 3) / 6))


# Soft Shrink
def soft_shrink(x: Tensor, lm: float = 0.5) -> Tensor:
    return sign(x) * np.maximum(np.abs(x) - lm, 0)


# Производная Soft Shrink
def soft_shrink_derivative(x: Tensor, lm: float = 0.5) -> Tensor:
    return np.where(np.abs(x) > lm, sign(x), 0)


# Hard Shrink
def hard_shrink(x: Tensor, lm: float = 0.5) -> Tensor:
    return np.where(np.abs(x) < lm, 0, x)


# Производная Hard Shrink
def hard_shrink_derivative(x: Tensor, lm: float = 0.5) -> Tensor:
    return np.where(np.abs(x) < lm, 0, 1)


# Функция активации Sign
def sign(x: Tensor) -> Tensor:
    return np.sign(x)


# Производная функции активации Sign
def sign_derivative(x: Tensor) -> Tensor:
    return np.zeros_like(x)
