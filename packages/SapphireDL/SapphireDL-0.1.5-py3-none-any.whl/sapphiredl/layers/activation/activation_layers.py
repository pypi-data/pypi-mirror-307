from layers.activation import (
    ActivationLayer,
    hyp_tan, hyp_tan_derivative,
    sigmoid, sigmoid_derivative,
    relu, relu_derivative,
    leaky_relu, leaky_relu_derivative,
    elu, elu_derivative,
    softmax, softmax_derivative,
    gelu, gelu_derivative,
    swish, swish_derivative,
    se_lu, se_lu_derivative,
    mi_sh, mi_sh_derivative,
    soft_plus, soft_plus_derivative,
    hard_swish, hard_swish_derivative,
    soft_shrink, soft_shrink_derivative,
    hard_shrink, hard_shrink_derivative,
    sign, sign_derivative
)


# Гиперболический тангенс (гладкая активация)
class HypTan(ActivationLayer):
    def __init__(self):
        super().__init__(hyp_tan, hyp_tan_derivative)


# Сигма (гладкая активация с диапазоном от 0 до 1)
class Sigmoid(ActivationLayer):
    def __init__(self):
        super().__init__(sigmoid, sigmoid_derivative)


# Р.е.л.у. (Rectified Linear Unit) - активация с обрезкой отрицательных значений
class ReLu(ActivationLayer):
    def __init__(self):
        super().__init__(relu, relu_derivative)


# Линейная р.е.л.у. (Leaky ReLU) - позволяет небольшие отрицательные значения
class LeakyRelu(ActivationLayer):
    def __init__(self):
        super().__init__(leaky_relu, leaky_relu_derivative)


# Экспоненциальная линейная активация (ELU) - гладкая активация для отрицательных значений
class ELU(ActivationLayer):
    def __init__(self):
        super().__init__(elu, elu_derivative)


# Софт макс - активация для много классовой классификации
class Softmax(ActivationLayer):
    def __init__(self):
        super().__init__(softmax, softmax_derivative)


# Gaussian Error Linear Unit (GeLU) - гладкая активация с вероятностным подходом
class GeLu(ActivationLayer):
    def __init__(self):
        super().__init__(gelu, gelu_derivative)


# Swish - гладкая активация с нелинейным поведением
class Swish(ActivationLayer):
    def __init__(self):
        super().__init__(swish, swish_derivative)


# Scaled Exponential Linear Unit (S.E.L.U.) - сама нормализуется активация
class ScExLu(ActivationLayer):
    def __init__(self):
        super().__init__(se_lu, se_lu_derivative)


# MiSH - гладкая активация с улучшенной производительностью
class MiSH(ActivationLayer):
    def __init__(self):
        super().__init__(mi_sh, mi_sh_derivative)


# SoftPlus - гладкая версия ReLU
class SoftPlus(ActivationLayer):
    def __init__(self):
        super().__init__(soft_plus, soft_plus_derivative)


# HardSwish - упрощенная версия Swish для повышения производительности
class HardSwish(ActivationLayer):
    def __init__(self):
        super().__init__(hard_swish, hard_swish_derivative)


# SoftShrink - уменьшение значений с использованием гладкой функции
class SoftShrink(ActivationLayer):
    def __init__(self):
        super().__init__(soft_shrink, soft_shrink_derivative)


# HardShrink - жесткое уменьшение значений
class HardShrink(ActivationLayer):
    def __init__(self):
        super().__init__(hard_shrink, hard_shrink_derivative)


# Знак - возвращает знак входного значения (-1, 0 или 1)
class Sign(ActivationLayer):
    def __init__(self):
        super().__init__(sign, sign_derivative)
