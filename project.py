from datetime import datetime


class Freelancer:
    def __init__(self, full_name: str, password: str):
        self.name = full_name
        self.password = password
        self.list_project = []

    def add_project(self, name: str, description: str, deadline, income: int, cost: int, status: bool = False):
        try:
            self.get_project(name)
            raise NameError("This project already is!")
        except ModuleNotFoundError:
            self.list_project.append(Project(name, description, deadline, income, cost, status))

    def del_project(self, name: str):
        self.list_project.remove(self.get_project(name))

    def get_list_project(self):
        return self.list_project

    def get_general_income(self):
        income = 0
        for i in self.list_project:
            income += i.get_income()
        return income

    def get_general_costs(self):
        cost = 0
        for i in self.list_project:
            cost += i.get_cost()
        return cost

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_project(self, name: str):
        for project in self.list_project:
            if project.get_name() == name:
                return project
        raise ModuleNotFoundError("Project not found!")


class Project:
    def __init__(self, name: str, description: str, deadline, income: int, cost: int,
                 status: bool = False):
        self.name = name
        self.desc = description
        self.deadline = deadline
        self.income = income
        self.cost = cost
        self.status = status
        self.list_tasks = []

    def add_task(self, name: str, description: str, status: bool = False):
        try:
            self.get_task(name)
            raise NameError("This task already is!")
        except ModuleNotFoundError:
            self.list_tasks.append(Task(name, description, status))

    def del_task(self, name: str):
        self.list_tasks.remove(self.get_task(name))

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.desc = description

    def set_deadline(self, time: datetime.date):
        self.deadline = time

    def set_status(self, status: bool):
        self.status = status

    def set_income(self, income):
        self.income = income

    def set_cost(self, cost):
        self.cost = cost

    def get_name(self):
        return self.name

    def get_description(self):
        return self.desc

    def get_deadline(self):
        return self.deadline

    def get_income(self):
        return self.income

    def get_cost(self):
        return self.cost

    def get_status(self):
        return self.status

    def get_task(self, name):
        for task in self.list_tasks:
            if task.get_name() == name:
                return task
        raise ModuleNotFoundError("Task not found!")

    def get_list_tasks(self):
        return self.list_tasks


class Task:
    def __init__(self, name: str, description: str, status: bool = False):
        self.name = name
        self.desc = description
        self.status = status

    def set_name(self, name: str):
        self.name = name

    def set_description(self, description: str):
        self.desc = description

    def set_status(self, status: bool):
        self.status = status

    def get_name(self):
        return self.name

    def get_description(self):
        return self.desc

    def get_status(self):
        return self.status