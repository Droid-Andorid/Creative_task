import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from project import Freelancer
import os
import json
import pickle


class App(tk.Tk):
    __slots__ = "_all_frames"
    user: Freelancer

    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.wm_minsize(650, 470)
        self.title("Example title")
        self.protocol("WM_DELETE_WINDOW", self.destroy_app)
        self._main_frame = None
        self._all_frames = {}
        if self.check_auth():
            with open("Data/settings.json", "r") as f:
                settings: dict = json.loads(f.read())
                user_name = settings.get("user")
                with open(f"Data/DataUser/{user_name}.dat", "rb") as f:
                    user = pickle.load(f)
                    App.user = user
            self.switch_frames(MainFrame)
        else:
            self.switch_frames(WelcomeFrame)

    def switch_frames(self, frame_class):
        if self._main_frame:
            self._main_frame.pack_forget()

        frame = self._all_frames.get(frame_class, False)

        if not frame:
            frame = frame_class(self)

            self._all_frames[frame_class] = frame

        frame.pack(fill=tk.X, expand=True)
        frame.update()
        self._main_frame = frame

    def destroy_app(self):
        if os.path.exists("Data/settings.json"):
            if self.check_auth():
                self.destroy()
                return 
        else:
            self.destroy()
            return
        user_name = self.user.get_name()
        with open(f"Data/DataUser/{user_name}.dat", "wb") as f:
            pickle.dump(self.user, f, pickle.DEFAULT_PROTOCOL)

        self.destroy()

    def exit_account(self):
        with open("Data/settings.json", "w") as f:
            settings = {"user": "",
                        "authorization": False}
            f.write(json.dumps(settings))
        self.switch_frames(WelcomeFrame)

    def check_auth(self) -> bool:
        if os.path.exists("Data/settings.json"):
            with open("Data/settings.json", "r") as f:
                auth: dict = json.loads(f.read())
                return bool(auth.get("authorization"))
        return False


class WelcomeFrame(tk.Frame):
    __slots__ = "frame_btn"

    def __init__(self, master):
        super().__init__(master)
        self.lb_welcome = tk.Label(self,
                                   text="Ласкаво просимо. Цей додаток створений для відстеження виконання проектів "
                                        "та їх завдань")

        self.frame_btn = tk.Frame(self)
        self.btn_reg = tk.Button(self.frame_btn, text="Реєстрація", command=lambda: master.switch_frames(RegisterFrame))
        self.btn_login = tk.Button(self.frame_btn, text="Увійти", command=lambda: master.switch_frames(LoginFrame))

        self.lb_welcome.pack()
        self.frame_btn.pack(pady=15)
        self.btn_reg.pack(side=tk.LEFT, padx=20)
        self.btn_login.pack(side=tk.RIGHT, padx=20)


class RegisterFrame(tk.Frame):
    __slots__ = "frame_btn"

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.lb_name = tk.Label(self, text="Введіть нікнейм")
        self.field_name = tk.Entry(self)
        self.lb_pin = tk.Label(self, text="Введіть пароль")
        self.field_pin = tk.Entry(self)

        self.frame_btn = tk.Frame(self)
        self.btn_save = tk.Button(self.frame_btn, text="Зареєструватись", command=self.save_user)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(WelcomeFrame))

        self.lb_name.pack()
        self.field_name.pack()
        self.lb_pin.pack()
        self.field_pin.pack()
        self.frame_btn.pack(pady=15)
        self.btn_back.pack(side=tk.LEFT, padx=10)
        self.btn_save.pack(side=tk.RIGHT, padx=10)

    def save_user(self):
        if self.field_name.get() == "":
            self.lb_name.configure(fg="red")
            return
        elif self.field_pin.get() == "":
            self.lb_pin.configure(fg="red")
            self.lb_name.configure(fg="white")
            return
        if not os.path.exists("Data"):
            os.mkdir("Data")
        if not os.path.exists("Data/DataUser"):
            os.mkdir("Data/DataUser")

        user = Freelancer(self.field_name.get(), self.field_pin.get())
        self.master.user = user

        with open("Data/settings.json", "w") as f:
            settings = {"user": f"{self.field_name.get()}",
                        "authorization": True}
            f.write(json.dumps(settings))

        if not os.path.exists(f"Data/DataUser/{user.get_name()}.dat"):
            with open(f"Data/DataUser/{user.get_name()}.dat", "wb") as f:
                pickle.dump(user, f, pickle.HIGHEST_PROTOCOL)

        try:
            MainFrame.user_name.set(self.master.user.get_name())
        except AttributeError:
            pass

        self.master.switch_frames(MainFrame)


class LoginFrame(tk.Frame):
    __slots__ = "frame_btn"

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.info_var = tk.StringVar(self)
        self.lb_name = tk.Label(self, text="Введіть ваш нікнейм")
        self.field_name = tk.Entry(self)
        self.lb_pin = tk.Label(self, text="Введіть пароль")
        self.field_pin = tk.Entry(self)
        self.lb_info = tk.Label(self, textvariable=self.info_var, fg="red")

        self.frame_btn = tk.Frame(self)
        self.btn_save = tk.Button(self.frame_btn, text="Увійти", command=self.login)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(WelcomeFrame))

        self.lb_name.pack()
        self.field_name.pack()
        self.lb_pin.pack()
        self.field_pin.pack()
        self.lb_info.pack()
        self.frame_btn.pack(pady=15)
        self.btn_back.pack(side=tk.LEFT, padx=10)
        self.btn_save.pack(side=tk.RIGHT, padx=10)

    def login(self):
        if self.field_name.get() == "":
            self.lb_name.configure(fg="red")
            return
        elif self.field_pin.get() == "":
            self.lb_pin.configure(fg="red")
            self.lb_name.configure(fg="white")
            return

        if not os.path.exists("Data"):
            self.info_var.set("Наразі немає зареєстрованих користувачів")
            return

        if not os.path.exists(f"Data/DataUser/{self.field_name.get()}.dat"):
            self.info_var.set("Такого користувача не існує")
            return

        with open(f"Data/DataUser/{self.field_name.get()}.dat", "rb") as f:
            user = pickle.load(f)
            if self.field_pin.get() != user.get_password():
                self.info_var.set("Невірний пароль")
                return
            self.master.user = user

        with open("Data/settings.json", "w") as f:
            account = {"user": f"{self.field_name.get()}",
                       "authorization": True}
            f.write(json.dumps(account))
        try:
            MainFrame.user_name.set(self.master.user.get_name())
        except AttributeError:
            pass

        self.master.switch_frames(MainFrame)


class MainFrame(tk.Frame):
    __slots__ = ("frame", "frame_btn")
    user_name = None

    def __init__(self, master):
        super().__init__(master)
        self.frame = tk.Frame(self)
        MainFrame.user_name = tk.StringVar(value=self.master.user.get_name())
        self.lb_user_name = tk.Label(self.frame, textvariable=self.user_name)
        self.info_btn = tk.Button(self.frame, text="Інформація про проекти", command=lambda: master.switch_frames(DetailProject))
        self.btn_exit_acc = tk.Button(self.frame, text="Вихід з акаунту", command=master.exit_account)
        self.btn_exit_app = tk.Button(self.frame, text="Вихід з додатку", command=master.destroy_app)

        self.lb_title = tk.Label(self, text="Головна сторінка")

        self.frame_btn = tk.Frame(self)
        self.btn_add_project = tk.Button(self.frame_btn, text="Додати проект",
                                         command=lambda: master.switch_frames(AddProject))
        self.btn_del_project = tk.Button(self.frame_btn, text="Видалити проект",
                                         command=lambda: master.switch_frames(DelProject))
        self.btn_add_task = tk.Button(self.frame_btn, text="Додати завдання до проекту",
                                      command=lambda: master.switch_frames(AddTask))
        self.btn_del_task = tk.Button(self.frame_btn, text="Видалити завдання з проекту",
                                      command=lambda: master.switch_frames(DelTask))
        self.btn_change_project = tk.Button(self, text="Внести зміни в проект",
                                            command=lambda: master.switch_frames(ChangeProject))
        self.btn_change_task = tk.Button(self, text="Внести зміни в завдання",
                                         command=lambda: master.switch_frames(ChangeTask))

        self.frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH)
        self.lb_user_name.pack()
        self.info_btn.pack()
        self.btn_exit_acc.pack()
        self.btn_exit_app.pack()

        self.lb_title.pack()
        self.frame_btn.pack(pady=15)
        self.btn_add_project.pack(side=tk.LEFT, padx=10)
        self.btn_del_project.pack(side=tk.RIGHT, padx=10)
        self.btn_add_task.pack(padx=10, pady=5)
        self.btn_del_task.pack(padx=10, pady=5)
        self.btn_change_project.pack()
        self.btn_change_task.pack(pady=5)

class AddProject(tk.Frame):
    __slots__ = ("frame", "frame_btn")

    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Додати проект")

        self.frame = tk.Frame(self)

        self.lb_name = tk.Label(self.frame, text="Назва проекту")
        self.field_name = tk.Entry(self.frame)
        self.lb_deadline = tk.Label(self.frame, text="Дедлайн")
        self.field_deadline = tk.Entry(self.frame)
        self.lb_income = tk.Label(self.frame, text="Дохід від проекту")
        self.field_income = tk.Entry(self.frame)
        self.lb_cost = tk.Label(self.frame, text="Витрати на проект")
        self.field_cost = tk.Entry(self.frame)
        self.lb_desc = tk.Label(self.frame, text="Опис")
        self.field_desc = tk.Entry(self.frame)

        self.frame_btn = tk.Frame(self)
        self.btn_add = tk.Button(self.frame_btn, text="Додати проект", command=self.add_project)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.frame.pack()
        self.lb_name.grid(row=0, column=0, padx=10)
        self.field_name.grid(row=1, column=0, padx=10)
        self.lb_deadline.grid(row=2, column=0, padx=10)
        self.field_deadline.grid(row=3, column=0, padx=10)
        self.lb_income.grid(row=0, column=2, padx=10)
        self.field_income.grid(row=1, column=2, padx=10)
        self.lb_cost.grid(row=2, column=2, padx=10)
        self.field_cost.grid(row=3, column=2, padx=10)
        self.lb_desc.grid(row=0, column=1, padx=10)
        self.field_desc.grid(row=1, column=1, padx=10)
        self.frame_btn.pack(pady=10)
        self.btn_add.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def add_project(self):
        try:
            if self.field_income.get() == "" or self.field_income.get() == " ":
                income = 0
            else:
                income = int(self.field_income.get())
            if self.field_cost.get() == "" or self.field_cost.get() == " ":
                cost = 0
            else:
                cost = int(self.field_cost.get())
            App.user.add_project(self.field_name.get(), self.field_desc.get(), self.field_deadline.get(),
                                 income, cost)
            MainFrame.list_project = [i.get_name() for i in App.user.get_list_project()]
            showinfo("Operation saving", "Успішно виконано!")
        except NameError:
            showerror("NameError", "Такий проект вже існує!")
        except ValueError:
            showerror("ValueError", "В полі 'дохід' та 'витрати' повинні бути числа")


class DelProject(tk.Frame):
    __slots__ = "frame_btn"
    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Видалити проект")

        self.lb_name_project = tk.Label(self, text="Виберіть проект")
        self.name_project = tk.Entry(self)

        self.frame_btn = tk.Frame(self)
        self.btn_del = tk.Button(self.frame_btn, text="Видалити проект", command=self.del_project)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()

        self.btn_del.pack(side=tk.RIGHT)
        self.btn_back.pack(side=tk.LEFT)
        self.name_project.pack()
        self.frame_btn.pack()
        self.btn_del.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def del_project(self):
        try:
            self.master.user.del_project(self.name_project.get())
            showinfo("OperationSuccess", "Успішно виконано!")
        except ModuleNotFoundError:
            showerror("NotFoundError", "Проект не знайдено")


class AddTask(tk.Frame):
    __slots__ = ("frame", "frame_btn")
    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Додати завдання")

        self.lb_name_project = tk.Label(self, text="Назва проекту")
        self.name_project = tk.Entry(self)
        
        self.frame = tk.Frame(self)
        self.lb_name = tk.Label(self.frame, text="Назва завдання")
        self.field_name = tk.Entry(self.frame)
        self.lb_desc = tk.Label(self.frame, text="Опис")
        self.field_desc = tk.Entry(self.frame)

        self.frame_btn = tk.Frame(self)
        self.btn_add = tk.Button(self.frame_btn, text="Додати завдання", command=self.add_task)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.lb_name_project.pack()
        self.name_project.pack()
        self.frame.pack()
        self.lb_name.grid(row=0, padx=10)
        self.field_name.grid(row=1, padx=10)
        self.lb_desc.grid(row=0, column=1, padx=10)
        self.field_desc.grid(row=1, column=1, padx=10)
        self.frame_btn.pack()
        self.btn_add.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def add_task(self):
        if self.field_name.get() == "" or self.field_name.get() == " ":
            showerror("ValueError", "Напишіть назву завдання!")
            return
        try:
            App.user.get_project(self.name_project.get()).add_task(self.field_name.get(), self.field_desc.get())
            showinfo("OperationSuccess", "Успішно збережено")
        except NameError:
            showerror("NameError", "Це завдання вже існує")
        except ModuleNotFoundError:
            showerror("NotFoundError", "Такого проекту не існує")


class DelTask(tk.Frame):
    __slots__ = ("dropdown_task", "frame_btn")
    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Видалити завдання")

        self.list_tasks = ["Виберіть завдання"]
        self.select_task = tk.StringVar()
        self.select_task.set(self.list_tasks[0])

        self.lb_name_project = tk.Label(self, text="Назва проекту")
        self.name_project = tk.Entry(self)
        self.btn_select = tk.Button(self, text="Вибрати проект", command=self.check_select)

        self.dropdown_task = tk.OptionMenu(self, self.select_task, *self.list_tasks)

        self.frame_btn = tk.Frame(self)
        self.btn_del = tk.Button(self.frame_btn, text="Видалити завдання", command=self.del_task)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.lb_name_project.pack()
        self.name_project.pack()
        self.btn_select.pack()
        self.dropdown_task.pack()
        self.frame_btn.pack()
        self.btn_del.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def del_task(self):
        try:
            project = App.user.get_project(self.name_project.get())
            project.del_task(self.select_task.get())
            showinfo("OperationSuccess", "Завдання видалено")
        except ModuleNotFoundError:
            showerror("NotFoundError", "Завдання або проекту не існує!")

    def check_select(self):
        try:
            project = App.user.get_project(self.name_project.get())
            self.list_tasks = [task.get_name() for task in project.get_list_tasks()]
        except ModuleNotFoundError:
            showerror("NotFoundError", "Проекту не існує!")
            return

        menu = self.dropdown_task["menu"]
        menu.delete(0, "end")
        for string in self.list_tasks:
            menu.add_command(label=string, command=lambda value=string: self.select_task.set(value))


class ChangeProject(tk.Frame):
    __slots__ = ("frame", "dropdown_status", "frame_btn")
    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Внести зміни в проект")

        self.lb_name = tk.Label(self, text="Назва проекту")
        self.field_name = tk.Entry(self)

        self.frame = tk.Frame(self)
        self.lb_new_name = tk.Label(self.frame, text="Нова назва проекту")
        self.field_new_name = tk.Entry(self.frame)
        self.lb_desc = tk.Label(self.frame, text="Новий опис")
        self.field_desc = tk.Entry(self.frame)
        self.lb_deadline = tk.Label(self.frame, text="Новий дедлайн")
        self.field_deadline = tk.Entry(self.frame)
        self.lb_income = tk.Label(self.frame, text="Новий дохід")
        self.field_income = tk.Entry(self.frame)
        self.lb_cost = tk.Label(self.frame, text="Нові витрати")
        self.field_cost = tk.Entry(self.frame)
        self.lb_status = tk.Label(self.frame, text="Новий статус проекту")
        self.select_status = tk.StringVar()
        list_status = ("True", "False")
        self.dropdown_status = tk.OptionMenu(self.frame, self.select_status, *list_status)

        self.frame_btn = tk.Frame(self)
        self.btn_change = tk.Button(self.frame_btn, text="Внести зміни", command=self.enter_change)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.lb_name.pack()
        self.field_name.pack()
        self.frame.pack()
        self.lb_new_name.grid(row=0, column=0, padx=10)
        self.field_new_name.grid(row=1, column=0, padx=10)
        self.lb_desc.grid(row=2, column=0, padx=10)
        self.field_desc.grid(row=3, column=0, padx=10)
        self.lb_deadline.grid(row=0, column=1, padx=10)
        self.field_deadline.grid(row=1, column=1, padx=10)
        self.lb_status.grid(row=2, column=1, padx=10)
        self.dropdown_status.grid(row=3, column=1, padx=10)
        self.lb_income.grid(row=0, column=2, padx=10)
        self.field_income.grid(row=1, column=2, padx=10)
        self.lb_cost.grid(row=2, column=2, padx=10)
        self.field_cost.grid(row=3, column=2, padx=10)
        self.frame_btn.pack()
        self.btn_change.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def enter_change(self):
        try:
            project = self.master.user.get_project(self.field_name.get())
            if self.field_income.get() != "" and self.field_income.get() != " ":
                project.set_income(int(self.field_income.get()))
            if self.field_cost.get() != "" and self.field_cost.get() != " ":
                project.set_cost(int(self.field_cost.get()))
            if self.field_new_name.get() != "" and self.field_new_name.get() != " ":
                project.set_name(self.field_new_name.get())
            if self.field_desc.get() != "" and self.field_desc.get() != " ":
                project.set_description(self.field_desc.get())
            if self.field_deadline.get() != "" and self.field_deadline.get() != " ":
                project.set_deadline(self.field_deadline.get())
            if self.select_status.get() != "":
                project.set_status(bool(self.select_status.get()))
            showinfo("OperationSuccess", "Успішно збережено")
        except ModuleNotFoundError:
            showerror("NotFoundError", "Не знайдено проекту")
        except ValueError:
            showerror("ValueError", "В полі 'дохід' та 'витрати' повинні бути числа")

class ChangeTask(tk.Frame):
    __slots__ = ("frame", "dropdown_task", "frame_btn")

    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Внести зміни в завдання")

        self.frame = tk.Frame(self)
        self.lb_name_project = tk.Label(self.frame, text="Назва проекта")
        self.field_name_project = tk.Entry(self.frame)
        self.lb_name = tk.Label(self.frame, text="Назва завдання")
        self.field_name = tk.Entry(self.frame)
        self.lb_new_name = tk.Label(self.frame, text="Нова назва завдання")
        self.field_new_name = tk.Entry(self.frame)
        self.lb_desc = tk.Label(self.frame, text="Новий опис")
        self.field_desc = tk.Entry(self.frame)
        self.lb_status = tk.Label(self.frame, text="Новий статус завдання")
        self.select_status = tk.StringVar()
        list_status = ("True", "False")
        self.dropdown_status = tk.OptionMenu(self.frame, self.select_status, *list_status)

        self.frame_btn = tk.Frame(self)
        self.btn_change = tk.Button(self.frame_btn, text="Внести зміни", command=self.enter_change)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.frame.pack()
        self.lb_name_project.grid(row=0, column=0, padx=10)
        self.field_name_project.grid(row=1, column=0, padx=10)
        self.lb_name.grid(row=2, column=0, padx=10)
        self.field_name.grid(row=3, column=0, padx=10)
        self.lb_new_name.grid(row=0, column=1, padx=10)
        self.field_new_name.grid(row=1,column=1, padx=10)
        self.lb_desc.grid(row=2, column=1, padx=10)
        self.field_desc.grid(row=3, column=1, padx=10)
        self.lb_status.grid(row=4, column=1, padx=10)
        self.dropdown_status.grid(row=5, column=1, padx=10)
        self.frame_btn.pack()
        self.btn_change.pack(side=tk.RIGHT, padx=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)

    def enter_change(self):
        try:
            task = self.master.user.get_project(self.field_name_project.get()).get_task(self.field_name.get())
            if self.field_new_name.get() != "" and self.field_new_name.get() != " ":
                task.set_name(self.field_new_name.get())
            if self.field_desc.get() != "" and self.field_desc.get() != " ":
                task.set_description(self.field_desc.get())
            if self.select_status.get() != "":
                task.set_status(bool(self.select_status.get()))
            showinfo("OperationSuccess", "Успішно збережено")
        except ModuleNotFoundError:
            showerror("NotFoundError", "Не знайдено проекту або завдання")



class DetailProject(tk.Frame):
    __slots__ = ("frame", "dropdown_tasks", "frame_btn")
    def __init__(self, master):
        super().__init__(master)
        self.lb_title = tk.Label(self, text="Інформація про проекти")

        self.frame = tk.Frame(self)
        self.lb_name_project = tk.Label(self.frame, text="Назва проекту")
        self.select_project = tk.StringVar(self)
        self.select_project.trace_add("write", self.check_select)
        if len(master.user.get_list_project()) >= 1:
            self.list_projects = [p.get_name() for p in master.user.get_list_project()]
        else:
            self.list_projects = ["Виберіть проект"]
        self.dropdown_projects = tk.OptionMenu(self.frame, self.select_project, *self.list_projects)
        self.btn_project_i = tk.Button(self.frame, text="Отримати інформацію", command=self.project_info)
        self.lb_name_task = tk.Label(self.frame, text="Назва завдання")
        self.select_task = tk.StringVar(self)
        self.list_tasks = ["Виберіть завдання"]
        self.dropdown_tasks = tk.OptionMenu(self.frame, self.select_task, *self.list_tasks)
        self.btn_task_i = tk.Button(self.frame, text="Отримати інформацію", command=self.task_info)

        self.info_text = tk.Text(self, height=16)
        self.frame_btn = tk.Frame(self)
        self.btn_upd = tk.Button(self.frame_btn, text="Оновити списки", command=self.update_lists)
        self.btn_back = tk.Button(self.frame_btn, text="Назад", command=lambda: master.switch_frames(MainFrame))

        self.lb_title.pack()
        self.frame.pack()
        self.lb_name_project.grid(row=0, column=0, pady =10)
        self.dropdown_projects.grid(row=1, column=0, pady=10)
        self.btn_project_i.grid(row=2, column=0, pady=10, padx=10)
        self.lb_name_task.grid(row=0, column=1, pady=10)
        self.dropdown_tasks.grid(row=1, column=1, pady=10)
        self.btn_task_i.grid(row=2, column=1, pady=10, padx=10)
        self.info_text.pack(padx=15)
        self.frame_btn.pack(pady=10)
        self.btn_back.pack(side=tk.LEFT, padx=10)
        self.btn_upd.pack(side=tk.RIGHT, padx=10)

    def check_select(self, var, index, mode):
        self.list_tasks = [t.get_name() for t in self.master.user.get_project(self.select_project.get()).get_list_tasks()]

        menu = self.dropdown_tasks["menu"]
        menu.delete(0, "end")
        for string in self.list_tasks:
            menu.add_command(label=string, command=lambda value=string: self.select_task.set(value))

    def project_info(self):
        self.info_text.delete("1.0", tk.END)
        project = self.master.user.get_project(self.select_project.get())
        if len(project.get_list_tasks()) > 3:
            tasks = [t.get_name() for t in project.get_list_tasks()[:3]]
            tasks.append(f"....+{len(project.get_list_tasks()[3:])}")
        else:
            tasks = [t.get_name() for t in project.get_list_tasks()]

        self.info_text.insert(tk.END,
                              chars=f"Name: {project.get_name()}\n"
                                    f"Description: {project.get_description()}\n"
                                    f"Deadline: {project.get_deadline()}\n"
                                    f"Income: {project.get_income()}\n"
                                    f"Cost: {project.get_cost()}\n"
                                    f"Tasks: {tasks}\n"
                                    f"Status: {'Complete' if project.get_status() else 'In progress...'}")

    def task_info(self):
        self.info_text.delete("1.0", tk.END)
        task = self.master.user.get_project(self.select_project.get()).get_task(self.select_task.get())
        self.info_text.insert(tk.END,
                              chars=f"Name: {task.get_name()}\n"
                                    f"Description: {task.get_description()}\n"
                                    f"Status: {'Complete' if task.get_status() else 'In progress'}")

    def update_lists(self):
        self.list_projects = [p.get_name() for p in self.master.user.get_list_project()]

        menu = self.dropdown_projects["menu"]
        menu.delete(0, "end")
        for string in self.list_projects:
            menu.add_command(label=string, command=lambda value=string: self.select_project.set(value))


if __name__ == "__main__":
    app = App()
    app.mainloop()
