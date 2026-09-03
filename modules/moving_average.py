# modules/moving_average.py
"""Модуль прогноза методом скользящей средней (Принцип OCP: легко расширить)"""
import numpy as np

class MovingAverageForecaster:
    """Класс экстраполяции по скользящей средней"""
    def __init__(self, window_size: int):
        if window_size < 2:
            raise ValueError("Окно прогноза должно быть >= 2")
        self.n = window_size

    def predict(self, values: list, steps: int) -> list:
        """
        Прогнозирует steps шагов вперёд.
        Каждый следующий шаг использует предыдущий прогноз (как в методичке).
        """
        extended = values.copy()
        forecast = []
        for _ in range(steps):
            window = extended[-self.n:]
            next_val = float(np.mean(window))
            forecast.append(next_val)
            extended.append(next_val)  # добавляем прогноз в ряд для следующего шага
        return forecast