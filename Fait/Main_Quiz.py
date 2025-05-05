# main.py
import tkinter as tk
from tkinter import messagebox
import random
# import winsound

from quiz_manager import load_questions, get_random_question

LEVEL_TIME = {
    "easy": 15,
    "medium": 10,
    "hard": 5
}

BACKGROUND_COLOR = "#f0f0f0"
BUTTON_COLOR = "#4CAF50"
WARNING_COLOR = "#FF5722"
TEXT_COLOR = "#333333"

class QuizApp:
    def __init__(self, root):  # Correction ici __init__
        self.root = root
        self.root.title("Quiz Game - La Table Étoilée")
        self.root.geometry("700x500")
        self.root.config(bg=BACKGROUND_COLOR)

        self.score = 0
        self.current_question = None
        self.questions = []
        self.level = None
        self.timer_label = None
        self.score_label = None
        self.time_left = 0
        self.timer_id = None
        self.answer_buttons = []
        self.blinking = False

        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()
        title = tk.Label(self.root, text="🎯 Bienvenue dans le Quiz !", font=("Helvetica", 24, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        title.pack(pady=30)

        level_label = tk.Label(self.root, text="Choisissez un niveau :", font=("Helvetica", 16), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        level_label.pack(pady=20)

        easy_btn = tk.Button(self.root, text="Facile", width=20, height=2, bg=BUTTON_COLOR, fg="white", font=("Helvetica", 14),
                             command=lambda: self.start_quiz("easy"))
        easy_btn.pack(pady=10)

        medium_btn = tk.Button(self.root, text="Moyen", width=20, height=2, bg=BUTTON_COLOR, fg="white", font=("Helvetica", 14),
                               command=lambda: self.start_quiz("medium"))
        medium_btn.pack(pady=10)

        hard_btn = tk.Button(self.root, text="Difficile", width=20, height=2, bg=BUTTON_COLOR, fg="white", font=("Helvetica", 14),
                             command=lambda: self.start_quiz("hard"))
        hard_btn.pack(pady=10)

    def start_quiz(self, level):
        self.score = 0
        self.level = level
        try:
            self.questions = load_questions(f"data/questions/{level}.json")
            self.show_question()
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"Fichier de questions pour le niveau '{level}' introuvable.")

    def show_question(self):
        self.clear_screen()
        self.answer_buttons = []

        if not self.questions:
            self.end_game()
            return

        self.current_question = get_random_question(self.questions)
        self.questions.remove(self.current_question)

        q_text = self.current_question["question"]
        question_label = tk.Label(self.root, text=q_text, font=("Helvetica", 18, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, wraplength=600, justify="center")
        question_label.pack(pady=30)

        options = self.current_question["options"]
        for idx, option in enumerate(options):
            btn = tk.Button(self.root, text=option, width=30, height=2, bg=BUTTON_COLOR, fg="white", font=("Helvetica", 13),
                            command=lambda i=idx: self.check_answer(i))
            btn.pack(pady=8)
            self.answer_buttons.append(btn)

        self.time_left = LEVEL_TIME[self.level]
        self.timer_label = tk.Label(self.root, text=f"⏰ Temps restant : {self.time_left} s", font=("Helvetica", 16), fg="#ff5722", bg=BACKGROUND_COLOR)
        self.timer_label.pack(pady=15)

        self.score_label = tk.Label(self.root, text=f"🏆 Score actuel : {self.score}", font=("Helvetica", 16), fg="#2196F3", bg=BACKGROUND_COLOR)
        self.score_label.pack()

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"⏰ Temps restant : {self.time_left} s")
        if self.time_left > 0:
            if self.time_left <= 3:
                self.start_blinking()
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            messagebox.showwarning("Temps écoulé !", "⏰ Vous n'avez pas répondu à temps.")
            self.show_question()

    def start_blinking(self):
        if not self.blinking:
            self.blinking = True
            self.blink_buttons()

    def blink_buttons(self):
        if not self.blinking:
            return
        for btn in self.answer_buttons:
            current_color = btn.cget("bg")
            new_color = WARNING_COLOR if current_color == BUTTON_COLOR else BUTTON_COLOR
            btn.config(bg=new_color)
        self.root.after(400, self.blink_buttons)

    def stop_blinking(self):
        self.blinking = False
        for btn in self.answer_buttons:
            btn.config(bg=BUTTON_COLOR)

    def check_answer(self, selected_index):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.stop_blinking()

        correct = self.current_question["correct_answer"]
        if selected_index == correct:
            self.score += 1
            # winsound.MessageBeep(winsound.MB_ICONASTERISK)  # Son bonne réponse
            messagebox.showinfo("Bonne réponse !", "✅ Bravo !")
        else:
            # winsound.MessageBeep(winsound.MB_ICONHAND)  # Son mauvaise réponse
            explication = self.current_question["explanation"]
            messagebox.showerror("Mauvaise réponse", f"❌ Mauvaise réponse.\n\nExplication :\n{explication}")

        self.show_question()

    def end_game(self):
        self.clear_screen()

        end_label = tk.Label(self.root, text="🏁 Quiz terminé !", font=("Helvetica", 24, "bold"), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
        end_label.pack(pady=30)

        score_label = tk.Label(self.root, text=f"Votre score final : {self.score}", font=("Helvetica", 20), fg="#4CAF50", bg=BACKGROUND_COLOR)
        score_label.pack(pady=10)

        restart_btn = tk.Button(self.root, text="Revenir au menu", width=20, height=2, font=("Helvetica", 14), bg=BUTTON_COLOR, fg="white",
                                command=self.create_home_screen)
        restart_btn.pack(pady=30)

    def clear_screen(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.stop_blinking()
        for widget in self.root.winfo_children():
            widget.destroy()

# Lancer l'application
if __name__ == "__main__":  # Correction ici __name__ et __main__
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
