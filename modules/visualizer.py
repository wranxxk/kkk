# modules/visualizer.py
"""Визуализация с интерактивным графиком и экспортом"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

class RunVisualizer:
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.fig = plt.Figure(figsize=(7, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Панель инструментов для масштабирования и выбора периодов
        toolbar = NavigationToolbar2Tk(self.canvas, parent)
        toolbar.update()
        toolbar.pack(fill=tk.X)

    def plot(self, df, param1: str, param2: str, forecast: list = None):
        """Строит 2 графика + прогноз (если передан)"""
        self.fig.clear()
        ax1 = self.fig.add_subplot(2, 1, 1)
        ax2 = self.fig.add_subplot(2, 1, 2)
        
        # График 1
        ax1.plot(df['day_num'], df[param1], 'o-', label=param1, color='teal')
        if forecast:
            future_days = range(df['day_num'].max() + 1, df['day_num'].max() + 1 + len(forecast))
            ax1.plot(future_days, forecast, 's--', label=f'Прогноз ({param1})', color='red')
        ax1.set_title(f'Зависимость {param1} от дня')
        ax1.grid(True)
        ax1.legend()

        # График 2
        ax2.plot(df['day_num'], df[param2], 's-', label=param2, color='green')
        ax2.set_title(f'Зависимость {param2} от дня')
        ax2.grid(True)
        ax2.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def export(self, filepath: str):
        """Экспорт в PNG/PDF"""
        self.fig.savefig(filepath, dpi=150, bbox_inches='tight')
