import unittest
import os
from unittest.mock import patch
from todo_manager import Task, TaskManager

class TestTask(unittest.TestCase):
    def test_to_dict(self):
        task = Task(1, "Купить хлеб", False)
        self.assertEqual(task.to_dict(), {"id": 1, "title": "Купить хлеб", "done": False})

    def test_from_dict(self):
        data = {"id": 1, "title": "Купить хлеб", "done": False}
        task = Task.from_dict(data)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Купить хлеб")
        self.assertFalse(task.done)

    def test_from_dict_done_true(self):
        data = {"id": 5, "title": "Сделано", "done": True}
        task = Task.from_dict(data)
        self.assertTrue(task.done)

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tasks.json"
        self.test_task = TaskManager(self.test_file)

    def tearDown(self):
        # Удаляем временный файл после каждого теста
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_see_task(self):
        with patch('sys.stdout'), patch('builtins.input', return_value=""):
            self.test_task.see_task()

    def test_add_task(self):
        # Подменяем input, чтобы он вернул "Купить хлеб"
        with patch('builtins.input', return_value="Купить хлеб"):
            self.test_task.add_task()
        # Проверяем, что задача добавилась
        self.test_task.storage.load()
        self.assertEqual(len(self.test_task.storage.items), 1)
        self.assertEqual(self.test_task.storage.items[0].title, "Купить хлеб")
        self.assertEqual(self.test_task.storage.items[0].id, 1)  # первый id = 1

    def test_add_task_empty_title(self):
        with patch('builtins.input', side_effect=["", "Купить хлеб"]):
            self.test_task.add_task()
        self.test_task.storage.load()
        self.assertEqual(len(self.test_task.storage.items), 1)
        self.assertEqual(self.test_task.storage.items[0].title, "Купить хлеб")

    def test_check_task_true(self):
        with patch('builtins.input', side_effect=["Купить хлеб", "Вынести мусор"]):
            self.test_task.add_task()
            self.test_task.add_task()
        with patch('builtins.input', return_value="1"):
            self.test_task.check_task()
        self.assertEqual(self.test_task.storage.items[0].title, "Купить хлеб")
        self.assertTrue(self.test_task.storage.items[0].done)
        self.assertFalse(self.test_task.storage.items[1].done)

    def test_check_task_invalid_id(self):
        with patch('builtins.input', side_effect=["Купить хлеб", "Вынести мусор"]):
            self.test_task.add_task()
            self.test_task.add_task()
        # Первый ввод — "0" (неверный), второй — "1" (выйти из цикла)
        with patch('builtins.input', side_effect=["0", "2"]):
            self.test_task.check_task()
        self.assertFalse(self.test_task.storage.items[0].done)
        self.assertTrue(self.test_task.storage.items[1].done)

    def test_check_task_non_numeric(self):
        with patch('builtins.input', side_effect=["Купить хлеб"]):
            self.test_task.add_task()
        # Первый ввод — буква, второй — валидный id
        with patch('builtins.input', side_effect=["abc", "1"]):
            self.test_task.check_task()
        self.assertTrue(self.test_task.storage.items[0].done)

    def test_check_task_empty_storage(self):
        with patch('builtins.input', return_value="1"):
            self.test_task.check_task()
        self.assertEqual(len(self.test_task.storage.items), 0)
        self.assertEqual(self.test_task.next_id, 0)

    def test_del_task(self):
        with patch('builtins.input', side_effect=["Купить хлеб", "Вынести мусор", "Выключить утюг"]):
            self.test_task.add_task()
            self.test_task.add_task()
            self.test_task.add_task()
        with patch('builtins.input', return_value="1"):
            self.test_task.del_task()
        self.test_task.storage.load()
        self.assertEqual(len(self.test_task.storage.items), 2)
        self.assertEqual(self.test_task.storage.items[0].title, "Вынести мусор")
        self.assertEqual(self.test_task.storage.items[1].title, "Выключить утюг")
        self.assertEqual(self.test_task.storage.items[0].id, 1)
        self.assertEqual(self.test_task.storage.items[1].id, 2)

    def test_del_task_invalid_id(self):
        with patch('builtins.input', side_effect=["Купить хлеб", "Вынести мусор", "Выключить утюг"]):
            self.test_task.add_task()
            self.test_task.add_task()
            self.test_task.add_task()
        # Первый ввод — "0" (неверный), второй — "1" (выйти из цикла)
        with patch('builtins.input', side_effect=["0", "1"]):
            self.test_task.del_task()
        self.assertEqual(len(self.test_task.storage.items), 2)
        self.assertNotEqual(self.test_task.storage.items[0].id, 0)

    def test_del_task_non_numeric(self):
        with patch('builtins.input', side_effect=["Купить хлеб"]):
            self.test_task.add_task()
        with patch('builtins.input', side_effect=["abc", "1"]):
            self.test_task.del_task()
        self.assertEqual(len(self.test_task.storage.items), 0)

    def test_del_task_empty_storage(self):
        with patch('builtins.input', return_value="1"):
            self.test_task.del_task()
        self.assertEqual(len(self.test_task.storage.items), 0)
        self.assertEqual(self.test_task.next_id, 0)

    def test_add_multiple_tasks_id_increments(self):
        with patch('builtins.input', side_effect=["Первая", "Вторая", "Третья"]):
            self.test_task.add_task()
            self.test_task.add_task()
            self.test_task.add_task()
        self.test_task.storage.load()
        self.assertEqual(len(self.test_task.storage.items), 3)
        self.assertEqual(self.test_task.storage.items[0].id, 1)
        self.assertEqual(self.test_task.storage.items[1].id, 2)
        self.assertEqual(self.test_task.storage.items[2].id, 3)

if __name__ == '__main__':
    unittest.main()