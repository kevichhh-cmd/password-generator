import tkinter as tk
from tkinter import ttk
import random
import string
import math
import pyperclip
import time

DEFAULT_SPECIALS = "!@#$%^&*()"

def generate_password(length=12, letters=True, digits=True, specials=True):
    chars = ""
    if letters:
        chars += string.ascii_letters
    if digits:
        chars += string.digits
    if specials:
        chars += DEFAULT_SPECIALS
    if not chars:
        return None
    return "".join(random.choice(chars) for _ in range(length))

def estimate_entropy(length, pool_size):
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)

def strength_label(entropy_bits):
    if entropy_bits < 28:
        return "Очень слабый"
    elif entropy_bits < 36:
        return "Слабый"
    elif entropy_bits < 60:
        return "Средний"
    else:
        return "Сильный"

def assess_password(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in DEFAULT_SPECIALS for c in password):
        pool += len(DEFAULT_SPECIALS)
    others = [c for c in password if not (c.isalnum() or c in DEFAULT_SPECIALS)]
    pool += len(set(others))
    pool = max(pool, 1)
    entropy = estimate_entropy(len(password), pool)
    return {
        "entropy_bits": round(entropy, 2),
        "label": strength_label(entropy),
        "pool": pool
    }

class HoverButton(tk.Button):
    def __init__(self, master, hover_bg=None, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.default_bg = self["bg"]
        self.hover_bg = hover_bg if hover_bg else self.default_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_bg

    def on_leave(self, e):
        self['bg'] = self.default_bg

class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.theme = "light"

        # Фоны и цвета
        self.bg_light = "#abc6e2"
        self.bg_dark = "#191929"
        self.fg_light = "#000000"
        self.fg_dark = "#ffffff"
        self.button_bg = "#4CAF50"
        self.button_hover = "#45a049"
        self.button_red = "#f44336"
        self.button_red_hover = "#d32f2f"
        self.button_fg = "#ffffff"

        self.history = []
        self.cat_messages_shown = False
        self.rocket_messages_shown = False
        self.cat_messages = [
            "😼 Кот говорит: Используй сложные пароли!",
            "😼 Кот шепчет: Никому не показывай свой пароль!",
            "😼 Кот советует: Меняй пароль регулярно!",
            "😼 Кот шепчет: Не используй один пароль для всех сайтов!",
            "😼 Кот говорит: Смешивай буквы, цифры и символы!"
        ]
        self.rocket_messages = [
            "🚀 Подсказка: Используй разные символы для надежного пароля.",
            "🚀 Подсказка: Не используй один пароль везде.",
            "🚀 Подсказка: Меняй пароль каждые 2–3 месяца.",
            "🚀 Подсказка: Сильные пароли делают тебя безопаснее.",
            "🚀 Подсказка: Никому не делись своими паролями."
        ]

        self.show_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def switch_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        bg_color = self.bg_light if self.theme=="light" else self.bg_dark
        fg_color = self.fg_light if self.theme=="light" else self.fg_dark
        self.root.configure(bg=bg_color)

        theme_btn = tk.Button(self.root, text="🌗", command=self.switch_theme,
                              font=("Arial", 14), bd=0, bg=bg_color, fg=fg_color, activebackground=bg_color)
        theme_btn.place(x=460, y=10)

        tk.Label(self.root, text="Генератор паролей", font=("Bahnschrift Condensed", 24),
                 bg=bg_color, fg=fg_color).pack(pady=30)

        HoverButton(self.root, text="Сгенерировать пароль", font=("Bahnschrift Condensed", 16),
                    bg=self.button_bg, fg=self.button_fg, hover_bg=self.button_hover, width=25,
                    command=self.show_generator).pack(pady=10)

        HoverButton(self.root, text="Показать историю", font=("Bahnschrift Condensed", 16),
                    bg=self.button_bg, fg=self.button_fg, hover_bg=self.button_hover, width=25,
                    command=self.show_history).pack(pady=10)

        HoverButton(self.root, text="О программе", font=("Bahnschrift Condensed", 16),
                    bg=self.button_bg, fg=self.button_fg, hover_bg=self.button_hover, width=25,
                    command=self.show_about).pack(pady=10)

        HoverButton(self.root, text="Выход", font=("Bahnschrift Condensed", 16),
                    bg=self.button_red, fg=self.button_fg, hover_bg=self.button_red_hover, width=25,
                    command=self.root.destroy).pack(pady=10)

        # Добавляем интерактивные символы
        if self.theme=="light":
            # Кот
            self.cat_label = tk.Label(self.root, text="😼", font=("Arial", 32), bg=bg_color)
            self.cat_label.place(x=10, y=400)
            self.cat_label.bind("<Button-1>", self.cat_click)
        else:
            # Ракета
            self.rocket_label = tk.Label(self.root, text="🚀", font=("Arial", 32), bg=bg_color)
            self.rocket_label.place(x=10, y=400)
            self.rocket_label.bind("<Button-1>", self.rocket_click)


    def cat_click(self, event):
        if self.cat_messages_shown:
            return
        self.cat_messages_shown = True
        msg = random.choice(self.cat_messages)
        # сохраняем сообщение в истории (без пароля)
        self.history.append({"password": None, "label": msg, "entropy": None})
        # Анимация кота
        self.animate_cat(event.widget)

    def rocket_click(self, event):
        if self.rocket_messages_shown:
            return
        self.rocket_messages_shown = True
        msg = random.choice(self.rocket_messages)
        self.history.append({"password": None, "label": msg, "entropy": None})
        # Анимация ракеты: реактивные искры
        self.animate_rocket(event.widget)

    # ======= анимация кота: подпрыгивание + сердечко =======
    def animate_cat(self, widget):
        # координаты стартовые
        try:
            x0 = widget.winfo_x()
            y0 = widget.winfo_y()
        except Exception:
            x0, y0 = 10, 400

        peak = y0 - 50
        steps_up = 10
        steps_down = 12
        delay = 20  # ms

        # подпрыгивание вверх
        def up(step):
            if step > steps_up:
                show_heart()
                self.root.after(delay, lambda: down(0))
                return
            new_y = y0 - int((step/steps_up)*(y0 - peak))
            widget.place(x=x0, y=new_y)
            # лёгкое покачивание влево/вправо
            offset = (-1)**step * 3
            widget.place(x=x0 + offset, y=new_y)
            self.root.after(delay, lambda: up(step+1))

        # спуск вниз
        def down(step):
            if step > steps_down:
                widget.place(x=x0, y=y0)
                return
            new_y = peak + int((step/steps_down)*(y0 - peak))
            offset = (-1)**step * 2
            widget.place(x=x0 + offset, y=new_y)
            self.root.after(delay, lambda: down(step+1))

        # сердечко, которое всплывает и исчезает
        def show_heart():
            heart = tk.Label(self.root, text="❤️", font=("Arial", 18), bg=self.root["bg"], bd=0)
            heart_x = x0 + 20
            heart_y = peak - 10
            heart.place(x=heart_x, y=heart_y)

            def float_up(step_f=0):
                if step_f > 25:
                    heart.destroy()
                    return
                heart.place(x=heart_x, y=heart_y - step_f*3)
                # слегка уменьшаем яркость — просто уменьшаем насыщенность цвета текста (approx)
                # тк tkinter не поддерживает alpha для текста, просто плавно меняем color to light grey
                if step_f > 15:
                    heart.config(fg="#c0c0c0")
                self.root.after(40, lambda: float_up(step_f+1))

            float_up()

        up(0)

    # ======= анимация ракеты: реактивные искры =======
    def animate_rocket(self, widget):
        # координаты стартовые
        try:
            x0 = widget.winfo_x()
            y0 = widget.winfo_y()
        except Exception:
            x0, y0 = 10, 400

        # короткий подпрыг
        peak = y0 - 40
        steps = 8
        delay = 18

        def move_up(i=0):
            if i > steps:
                # запустить искры
                spawn_sparks()
                self.root.after(delay, lambda: move_down(0))
                return
            new_y = y0 - int((i/steps)*(y0 - peak))
            widget.place(x=x0, y=new_y)
            self.root.after(delay, lambda: move_up(i+1))

        def move_down(i=0):
            if i > steps:
                widget.place(x=x0, y=y0)
                return
            new_y = peak + int((i/steps)*(y0 - peak))
            widget.place(x=x0, y=new_y)
            self.root.after(delay, lambda: move_down(i+1))

        # спавн нескольких искр, каждая искра — маленький label с эмодзи, который летит вниз/вбок и исчезает
        sparks_emojis = ["💥", "⚡", "💨", "🔻"]
        def spawn_sparks():
            # создаём несколько вспышек с небольшим разбросом по X
            sparks = []
            for i in range(4):
                emo = random.choice(sparks_emojis)
                sx = x0 + 8 + random.randint(-6, 10)
                sy = y0 + 30 + random.randint(-2, 6)
                lbl = tk.Label(self.root, text=emo, font=("Arial", 14), bg=self.root["bg"], bd=0)
                lbl.place(x=sx, y=sy)
                sparks.append(lbl)

            # анимация для каждой искры
            def animate_spark(lbl, idx, step=0):
                # шаги: 0..10
                if step > 10:
                    try:
                        lbl.destroy()
                    except Exception:
                        pass
                    return
                # движение: вниз и немного в сторону
                dx = (-1)**idx * (step // 3)  # чередование направлений
                dy = step * 4
                lbl.place(x=lbl.winfo_x() + dx, y=lbl.winfo_y() + dy)
                # замедленное исчезновение: после нескольких шагов сделаем светлее (простая эмитация)
                if step > 6:
                    lbl.config(fg="#c0c0c0")
                self.root.after(45, lambda: animate_spark(lbl, idx, step+1))

            for idx, sp in enumerate(sparks):
                # немного с задержкой, чтобы был эффект последовательности
                self.root.after(idx * 60, lambda s=sp, i=idx: animate_spark(s, i, 0))

        move_up(0)

    def show_generator(self):
        self.clear_window()
        bg_color = self.bg_light if self.theme=="light" else self.bg_dark
        fg_color = self.fg_light if self.theme=="light" else self.fg_dark
        self.root.configure(bg=bg_color)

        tk.Label(self.root, text="Длина пароля:", font=("Bahnschrift Condensed", 16),
                 bg=bg_color, fg=fg_color).pack(pady=10)
        length_var = tk.IntVar(value=12)
        entry = tk.Entry(self.root, textvariable=length_var, font=("Bahnschrift Condensed", 14),
                         bd=2, relief="groove")
        entry.pack(pady=5)

        tk.Label(self.root, text="Выберите типы символов, которые будут включены в пароль:",
                 font=("Bahnschrift Condensed", 12), bg=bg_color, fg=fg_color, wraplength=450, justify="left").pack(pady=5)

        letters_var = tk.BooleanVar(value=True)
        digits_var = tk.BooleanVar(value=True)
        specials_var = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Буквы", variable=letters_var, font=("Bahnschrift Condensed", 14),
                       bg=bg_color, fg=fg_color, selectcolor=bg_color, bd=0, highlightthickness=0).pack(pady=5)
        tk.Checkbutton(self.root, text="Цифры", variable=digits_var, font=("Bahnschrift Condensed", 14),
                       bg=bg_color, fg=fg_color, selectcolor=bg_color, bd=0, highlightthickness=0).pack(pady=5)
        tk.Checkbutton(self.root, text="Спецсимволы", variable=specials_var, font=("Bahnschrift Condensed", 14),
                       bg=bg_color, fg=fg_color, selectcolor=bg_color, bd=0, highlightthickness=0).pack(pady=5)

        result_label = tk.Label(self.root, text="", font=("Bahnschrift Condensed", 14),
                                bg=bg_color, fg=fg_color, wraplength=450, justify="left")
        result_label.pack(pady=10)

        def generate_action():
            result_label.config(text="")
            try:
                length_val = int(length_var.get())
            except Exception:
                length_val = 12
            if length_val < 1:
                length_val = 12
            pw = generate_password(length_val, letters_var.get(), digits_var.get(), specials_var.get())
            if not pw:
                result_label.config(text="Ошибка: вы не выбрали ни один тип символов!")
                return
            assessment = assess_password(pw)
            try:
                pyperclip.copy(pw)
                copied = True
            except Exception:
                copied = False
            display_text = f"Пароль: {pw}\nНадёжность: {assessment['label']}\nЭнтропия: {assessment['entropy_bits']} бит"
            if copied:
                display_text += "\nПароль скопирован в буфер!"
            result_label.config(text="")
            for i in range(len(display_text)+1):
                result_label.config(text=display_text[:i])
                self.root.update()
                time.sleep(0.01)
            self.history.append({
                "password": pw,
                "entropy": assessment['entropy_bits'],
                "label": assessment['label']
            })

        HoverButton(self.root, text="Сгенерировать", font=("Bahnschrift Condensed", 16),
                    bg=self.button_bg, fg=self.button_fg, hover_bg=self.button_hover, width=20,
                    command=generate_action).pack(pady=10)
        HoverButton(self.root, text="Назад", font=("Bahnschrift Condensed", 16),
                    bg=self.button_red, fg=self.button_fg, hover_bg=self.button_red_hover, width=20,
                    command=self.show_main_menu).pack(pady=10)

    def show_history(self):
        self.clear_window()
        bg_color = self.bg_light if self.theme=="light" else self.bg_dark
        fg_color = self.fg_light if self.theme=="light" else self.fg_dark
        self.root.configure(bg=bg_color)

        tk.Label(self.root, text="История паролей", font=("Bahnschrift Condensed", 20),
                 bg=bg_color, fg=fg_color).pack(pady=10)

        history_text = tk.Text(self.root, font=("Bahnschrift Condensed", 14), bg=bg_color, fg=fg_color,
                               height=15, width=50, highlightthickness=0, bd=0)
        history_text.pack(pady=5)
        history_text.config(state=tk.DISABLED, takefocus=0)

        def load_history():
            history_text.config(state=tk.NORMAL)
            history_text.delete("1.0", tk.END)
            if not self.history:
                history_text.insert(tk.END, "Нет записей.\n")
            else:
                for idx, entry in enumerate(self.history, 1):
                    if entry.get("password"):
                        history_text.insert(tk.END,
                                            f"{idx}. Пароль: {entry['password']} | Надёжность: {entry['label']} | Энтропия: {entry['entropy']} бит\n")
                    else:
                        history_text.insert(tk.END,
                                            f"{idx}. {entry['label']}\n")
            history_text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(self.root, bg=bg_color)
        btn_frame.pack(pady=5)
        HoverButton(btn_frame, text="Показать", font=("Bahnschrift Condensed", 14),
                    bg=self.button_bg, fg=self.button_fg, hover_bg=self.button_hover, width=15, command=load_history).pack(side=tk.LEFT, padx=5)
        HoverButton(btn_frame, text="Очистить", font=("Bahnschrift Condensed", 14),
                    bg=self.button_red, fg=self.button_fg, hover_bg=self.button_red_hover, width=15,
                    command=lambda: [self.history.clear(), load_history()]).pack(side=tk.LEFT, padx=5)
        HoverButton(btn_frame, text="Назад", font=("Bahnschrift Condensed", 14),
                    bg=self.button_red, fg=self.button_fg, hover_bg=self.button_red_hover, width=15,
                    command=self.show_main_menu).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Все пароли сохраняются локально", font=("Bahnschrift Condensed", 12),
                 bg=bg_color, fg=fg_color).pack(pady=5)

    def show_about(self):
        self.clear_window()
        bg_color = self.bg_light if self.theme=="light" else self.bg_dark
        fg_color = self.fg_light if self.theme=="light" else self.fg_dark
        self.root.configure(bg=bg_color)

        tk.Label(self.root, text="О программе", font=("Bahnschrift Condensed", 24),
                 bg=bg_color, fg=fg_color).pack(pady=30)
        tk.Label(self.root, text="Программа для генерации паролей с оценкой надёжности.",
                 font=("Bahnschrift Condensed", 14), bg=bg_color, fg=fg_color, wraplength=450).pack(pady=10)
        tk.Label(self.root, text="Все пароли сохраняются локально", font=("Bahnschrift Condensed", 14),
                 bg=bg_color, fg=fg_color).pack(pady=10)

        HoverButton(self.root, text="Назад", font=("Bahnschrift Condensed", 16),
                    bg=self.button_red, fg=self.button_fg, hover_bg=self.button_red_hover, width=25,
                    command=self.show_main_menu).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
