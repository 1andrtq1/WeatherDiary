import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("700x500")

        self.data_file = "data.json"
        self.records = []
        self.load_data()

        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        # --- Поля ввода ---
        frame = tk.Frame(self.root)
        frame.pack(pady=10, fill=tk.X)

        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Температура:").grid(row=0, column=2, padx=5)
        self.temp_entry = tk.Entry(frame)
        self.temp_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Описание:").grid(row=0, column=4, padx=5)
        self.desc_entry = tk.Entry(frame)
        self.desc_entry.grid(row=0, column=5, padx=5)

        tk.Label(frame, text="Осадки:").grid(row=0, column=6, padx=5)
        self.rain_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Да", variable=self.rain_var).grid(row=0, column=7, padx=5)

        # --- Кнопки ---
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5, fill=tk.X)

        tk.Button(btn_frame, text="Добавить запись", command=self.add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Сохранить в JSON", command=self.save_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Загрузить из JSON", command=self.load_data_gui).pack(side=tk.LEFT, padx=5)

        # --- Фильтрация ---
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10, fill=tk.X)

        tk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5)
        self.filter_date = tk.Entry(filter_frame)
        self.filter_date.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Фильтр по температуре (>):").grid(row=0, column=2, padx=5)
        self.filter_temp = tk.Entry(filter_frame)
        self.filter_temp.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=5)

        # --- Список записей ---
        self.listbox = ttk.Treeview(self.root, columns=(1, 2, 3, 4), show='headings', height=15)
        self.listbox.heading(1, text="Дата")
        self.listbox.heading(2, text="Температура")
        self.listbox.heading(3, text="Описание")
        self.listbox.heading(4, text="Осадки")
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

    def add_record(self):
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        desc = self.desc_entry.get().strip()
        rain = "Да" if self.rain_var.get() else "Нет"

        # Валидация
        try:
            datetime.strptime(date, "%Y-%m-%d")
            if not date or not desc:
                raise ValueError("Дата и описание обязательны.")
            temp = float(temp)
            if temp < -100 or temp > 100:
                raise ValueError("Температура вне диапазона (-100..100).")
            if not desc:
                raise ValueError("Описание не может быть пустым.")
        except Exception as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return

        record = {"date": date, "temp": temp, "desc": desc, "rain": rain}
        self.records.append(record)
        self.update_listbox()

    def update_listbox(self):
        for i in self.listbox.get_children():
            self.listbox.delete(i)
        for rec in self.records:
            self.listbox.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], rec["rain"]))

    def apply_filter(self):
        f_date = self.filter_date.get().strip()
        f_temp = self.filter_temp.get().strip()

        filtered = self.records[:]

        if f_date:
            try:
                datetime.strptime(f_date, "%Y-%m-%d")
                filtered = [r for r in filtered if r["date"] == f_date]
            except:
                messagebox.showerror("Ошибка", "Неверный формат даты для фильтра.")
                return

        if f_temp:
            try:
                f_temp = float(f_temp)
                filtered = [r for r in filtered if r["temp"] > f_temp]
            except:
                messagebox.showerror("Ошибка", "Температура фильтра должна быть числом.")
                return

        for i in self.listbox.get_children():
            self.listbox.delete(i)
        for rec in filtered:
            self.listbox.insert("", "end", values=(rec["date"], rec["temp"], rec["desc"], rec["rain"]))

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранено", f"Данные сохранены в {self.data_file}")

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    self.records = json.load(f)
                except json.JSONDecodeError:
                    self.records = []
                    messagebox.showwarning("Ошибка", "Файл JSON повреждён. Создан новый.")
                    self.save_data()

    def load_data_gui(self):
        self.load_data()
        self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()