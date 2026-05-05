import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data_file = "weather_data.json"
        self.records = self.load_data()

        # Интерфейс ввода
        frame_input = tk.LabelFrame(root, text="Новая запись", padx=10, pady=10)
        frame_input.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.ent_date = tk.Entry(frame_input)
        self.ent_date.grid(row=0, column=1)

        tk.Label(frame_input, text="Температура (°C):").grid(row=1, column=0)
        self.ent_temp = tk.Entry(frame_input)
        self.ent_temp.grid(row=1, column=1)

        tk.Label(frame_input, text="Описание:").grid(row=2, column=0)
        self.ent_desc = tk.Entry(frame_input)
        self.ent_desc.grid(row=2, column=1)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(frame_input, text="Осадки", variable=self.precip_var).grid(row=3, columnspan=2)

        tk.Button(frame_input, text="Добавить запись", command=self.add_record).grid(row=4, columnspan=2, pady=5)

        # Интерфейс фильтрации
        frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        frame_filter.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_filter, text="Мин. Температура:").grid(row=0, column=0)
        self.ent_filter_temp = tk.Entry(frame_filter, width=10)
        self.ent_filter_temp.grid(row=0, column=1)
        
        tk.Button(frame_filter, text="Применить фильтр", command=self.update_table).grid(row=0, column=2, padx=5)
        tk.Button(frame_filter, text="Сброс", command=self.reset_filter).grid(row=0, column=3)

        # Таблица записей
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп. °C")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_table()

    def add_record(self):
        date = self.ent_date.get()
        temp = self.ent_temp.get()
        desc = self.ent_desc.get()
        precip = "Да" if self.precip_var.get() else "Нет"

        # Валидация
        if not date or not desc:
            messagebox.showerror("Ошибка", "Заполните дату и описание!")
            return
        try:
            temp_val = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return

        new_record = {"date": date, "temp": temp_val, "desc": desc, "precip": precip}
        self.records.append(new_record)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.ent_date.delete(0, tk.END)
        self.ent_temp.delete(0, tk.END)
        self.ent_desc.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        filter_temp = self.ent_filter_temp.get()
        
        for r in self.records:
            if filter_temp:
                try:
                    if r['temp'] < float(filter_temp): continue
                except: pass
            
            self.tree.insert("", tk.END, values=(r['date'], r['temp'], r['desc'], r['precip']))

    def reset_filter(self):
        self.ent_filter_temp.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
