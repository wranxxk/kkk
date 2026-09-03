# modules/statistics.py
"""Вспомогательная статистика (Инкапсуляция логики расчётов)"""
import pandas as pd

class RunStatistics:
    @staticmethod
    def weekend_distance(df: pd.DataFrame) -> float:
        """Сумма км за выходные (Sat, Sun)"""
        weekends = df[df['day_of_week'].isin(['Sat', 'Sun'])]
        return weekends['distance_km'].sum()

    @staticmethod
    def max_min_speed_change(df: pd.DataFrame) -> dict:
        """День с максимальным ростом и падением средней скорости"""
        df = df.copy()
        df['speed_diff'] = df['avg_speed'].diff()
        return {
            'max_up': {'day': int(df.loc[df['speed_diff'].idxmax(), 'day_num']), 'val': float(df['speed_diff'].max())},
            'max_down': {'day': int(df.loc[df['speed_diff'].idxmin(), 'day_num']), 'val': float(df['speed_diff'].min())}
        }