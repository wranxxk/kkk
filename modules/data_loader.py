# modules/data_loader.py
"""Модуль загрузки данных из JSON-файла (Принцип SRP: отвечает только за чтение)"""
import json
import pandas as pd
from pathlib import Path

class RunDataLoader:
    """Класс-загрузчик данных о пробежках"""
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.dataframe = None

    def load(self) -> pd.DataFrame:
        """Читает JSON, преобразует в DataFrame, добавляет номер дня"""
        if not self.filepath.exists():
            print(f"🔄 Загружаю данные из файла: {self.filepath}")
            raise FileNotFoundError(f"Файл не найден: {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            raw = json.load(f)
            
        self.dataframe = pd.DataFrame(raw['runs'])
        self.dataframe['date'] = pd.to_datetime(self.dataframe['date'])
        self.dataframe['day_num'] = range(1, len(self.dataframe) + 1)
        return self.dataframe