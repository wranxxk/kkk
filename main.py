# main.py
"""Основной GUI приложения (Вариант 1: Анализ пробежек)"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from modules.data_loader import RunDataLoader
from modules.moving_average import MovingAverageForecaster
from modules.visualizer import RunVisualizer
from modules.statistics import RunStatistics
import pandas as pd

class RunningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏃 Анализ пробежек ")
        self.root.geometry("1100x750")
        self.df = None

        self._build_ui()

    def _build_ui(self):
        # Верхняя панель
        top = ttk.Frame(self.root, padding="5")
        top.pack(fill=tk.X)
        ttk.Button(top, text="📂 Выбрать файл данных", command=self.load_data).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top, text="Период (n):").pack(side=tk.LEFT, padx=(20, 5))
        self.n_var = tk.IntVar(value=7)
        ttk.Spinbox(top, from_=2, to=15, textvariable=self.n_var, width=4).pack(side=tk.LEFT)
        
        ttk.Label(top, text="Прогноз (дней):").pack(side=tk.LEFT, padx=(20, 5))
        self.steps_var = tk.IntVar(value=3)
        ttk.Spinbox(top, from_=1, to=10, textvariable=self.steps_var, width=4).pack(side=tk.LEFT)
        
        ttk.Button(top, text="📈 Построить", command=self.plot_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(top, text="💾 Сохранить график", command=self.save_plot).pack(side=tk.LEFT)

        # Таблица
        tbl_frame = ttk.LabelFrame(self.root, text="📋 Данные", padding="5")
        tbl_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree = ttk.Treeview(tbl_frame, show='headings')
        scroll = ttk.Scrollbar(tbl_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Графики
        graph_frame = ttk.LabelFrame(self.root, text="📊 Графики (используйте лупу и кнопки ниже для масштабирования)", padding="5")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.viz = RunVisualizer(graph_frame)

        # Статус
        self.status = tk.StringVar(value="Готово к работе")
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN, anchor="w").pack(fill=tk.X)

    def load_data(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            loader = RunDataLoader(path)
            self.df = loader.load()
            self._fill_table()
            self.status.set(f"Загружено {len(self.df)} записей | Км за выходные: {RunStatistics.weekend_distance(self.df):.2f}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _fill_table(self):
        self.tree.delete(*self.tree.get_children())
        cols = list(self.df.columns)
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90, anchor="center")
        for _, row in self.df.iterrows():
            self.tree.insert("", tk.END, values=[row[c] for c in cols])

    def plot_data(self):
        if self.df is None:
            messagebox.showwarning("Внимание", "Сначала загрузите файл!")
            return
        try:
            n = self.n_var.get()
            steps = self.steps_var.get()
            forecaster = MovingAverageForecaster(window_size=n)
            forecast = forecaster.predict(self.df['distance_km'].tolist(), steps)
            self.viz.plot(self.df, 'distance_km', 'avg_speed', forecast)
            self.status.set(f"✅ Графики готовы | Прогноз на {steps} дн. (n={n})")
        except Exception as e:
            messagebox.showerror("Ошибка построения", str(e))

    def save_plot(self):
        if self.viz.fig is None: return
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("PDF", "*.pdf")])
        if path:
            self.viz.export(path)
            self.status.set(f"💾 График сохранён: {path}")

if __name__ == "__main__":
    root = tk.Tk()
    RunningApp(root)
    root.mainloop()