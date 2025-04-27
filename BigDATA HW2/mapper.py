#!/usr/bin/env python
import sys

# Чтение входных данных из стандартного потока ввода

for line in sys.stdin:

    # Разделение строки на столбцы
    data = line.strip().split(',')

    if len(data) == 16:
        # Извлечение цены в качестве значения
        price = data[9]

        # Вывод ключ-значение для передачи в reducer
        print("{0}t{1}".format("price", price))
