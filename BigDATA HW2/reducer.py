#!/usr/bin/env python



import sys
import numpy as np

# Инициализация переменных
total_count = 0
total_price = 0
total_price_squared = 0

# Чтение и обработка данных от mapper
for line in sys.stdin:

    key, value = line.strip().split('t')
    if key == "price":

        price = float(value)
        # Увеличение счетчика общего количества значений и общей суммы цен
        total_count += 1
        total_price += price
        total_price_squared += price ** 2

# Вычисление среднего значения и дисперсии
mean_price = total_price / total_count
variance_price = (total_price_squared / total_count) - (mean_price ** 2)

# Вывод результатов

print("Mean price: {:.2f}".format(mean_price))
print("Variance of price: {:.2f}".format(variance_price))
