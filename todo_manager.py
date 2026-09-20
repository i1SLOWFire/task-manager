from libs.console_menu.menu import ConsoleMenu
from libs.json_storage.storage import JSONStorage


class Task:
    def __init__(self, task_id, title, done=False):
        self.id = task_id
        self.title = title
        self.done = done

    def to_dict(self):
        # Превращает в словарь для JSON
        return {"id": self.id, "title": self.title, "done": self.done}

    @staticmethod
    def from_dict(data):
        # Создаёт задачу из словаря
        return Task(data["id"], data["title"], data["done"])


class TaskManager:
    def __init__(self, storage_name, password=None):
        self.next_id = 0
        self.menu_name = "menu.json"
        self.password = password
        self.menu = ConsoleMenu(self.menu_name, self, self.password)
        self.storage_name = storage_name
        self.storage = JSONStorage(self.storage_name, Task)

    def main(self):
        self.menu.play()

    def see_task(self):
        self.storage.load()
        for item in self.storage.items:
            if item.id == 0:
                print(item.title)
            elif not item.done:
                print(f"[ ] Задача №{item.id}: {item.title}")
            else:
                print(f"[X] Задача №{item.id}: {item.title}")
        input("\nНажмите Enter для того, чтобы продолжить.")

    def add_task(self):
        while True:
            self.storage.load()
            title = (input("Введите новую задачу: "))
            if title == "":
                print("Вы ничего не написали.")
                continue
            items = self.storage.items
            self.next_id = len(items) + 1
            self.storage.add_item(Task(self.next_id, title))
            return

    def check_task(self):
        while True:
            try:
                self.next_id = int(input("Введите номер выполненной задачи: "))
            except ValueError:
                print("Ошибка: введите число.")
                continue
            self.storage.load()
            if not self.storage.items:
                print("Список задач пуст.")
                return
            elif self.next_id < self.storage.items[0].id or self.next_id > len(self.storage.items):
                print("Задача с таким номером не найдена.")
                continue
            for item in self.storage.items:
                if item.id == self.next_id:
                    if item.done is True:
                        print('Задача была отмечена "выполненной" ранее!')
                        return
                    item.done = True
                    self.storage.save()
                    print("Задача выполнена!")
                    return

    def del_task(self):
        while True:
            try:
                self.next_id = int(input("Введите номер задачи, которую хотите удалить: "))
            except ValueError:
                print("Ошибка: введите число.")
                continue
            self.storage.load()
            if not self.storage.items:
                print("Список задач пуст.")
                return
            if self.next_id < self.storage.items[0].id or self.next_id > len(self.storage.items):
                print("Задача с таким номером не найдена.")
                continue
            for item in self.storage.items:
                if item.id == self.next_id:
                    self.storage.remove_item(item)
                    break
            for item in self.storage.items:
                if item.id > self.next_id:
                    item.id -= 1
            self.storage.save()
            return
