import tkinter as tk
from tkinter import messagebox
import random
import json
from datetime import datetime

class Question:
    def __init__(self, question, answers, correct):
        self.question = question
        self.answers = answers
        self.correct = correct

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Продвинутая викторина")
        self.questions = self.load_questions()
        self.score = 0
        self.current_question = 0

        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.radio_var = tk.IntVar()
        self.radio_var.set(-1)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.radio_var, value=i, font=("Arial", 12))
            self.radio_buttons.append(rb)
            rb.pack(anchor=tk.W)

        self.submit_button = tk.Button(root, text="Ответить", command=self.check_answer, font=("Arial", 12))
        self.submit_button.pack(pady=10)

        self.reset_button = tk.Button(root, text="Сбросить", command=self.reset_quiz, font=("Arial", 12), state=tk.DISABLED)
        self.reset_button.pack(pady=10)

        self.load_question()

    def load_questions(self):
        try:
            # Загрузка вопросов из файла
            with open("questions.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                questions = [Question(q["question"], q["answers"], q["correct"]) for q in data]
        except FileNotFoundError:
            # Пример вопросов, если файл не найден
            questions = [
                Question("Сколько будет 2 + 2?", ["3", "4", "5", "6"], 1),
                Question("Какая столица Франции?", ["Париж", "Мадрид", "Берлин", "Рим"], 0),
                Question("Как называется самый высокий горный хребет в мире?", ["Альпы", "Карпаты", "Гималаи", "Аппалачи"], 2)
            ]

        random.shuffle(questions)
        return questions

    def load_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data.question)
            answers = question_data.answers.copy()
            random.shuffle(answers)
            for i, answer in enumerate(answers):
                self.radio_buttons[i].config(text=answer)
        else:
            self.show_final_score()

    def check_answer(self):
        question_data = self.questions[self.current_question]
        user_answer = self.radio_var.get()
        if user_answer == question_data.correct:
            self.score += 1

        self.current_question += 1
        self.radio_var.set(-1)
        self.load_question()

        if self.current_question == len(self.questions):
            self.submit_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            self.save_result()

    def show_final_score(self):
        messagebox.showinfo("Результат", f"Ваш счет: {self.score} из {len(self.questions)}")

    def reset_quiz(self):
        self.current_question = 0
        self.score = 0
        random.shuffle(self.questions)
        self.load_question()
        self.submit_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

    def save_result(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = f"Дата: {now}, Счет: {self.score} из {len(self.questions)}"
        with open("results.txt", "a", encoding="utf-8") as file:
            file.write(result + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    quiz_app = QuizApp(root)
    root.mainloop()
