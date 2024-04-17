import time
import unittest
import project


class TestFreelancer(unittest.TestCase):
    def setUp(self):
        self.freelancer = project.Freelancer("TestUser", "")

    def generate_user(self):
        self.freelancer.add_project("TestProject", "TDesc", "TDls",
                                    100, 20)
        print("Generate user")

    def test_get_project(self):
        self.generate_user()
        self.assertEqual(self.freelancer.get_project("TestProject").get_name(), "TestProject")
        with self.assertRaises(ModuleNotFoundError):
            self.freelancer.get_project("TestProject1")

    def test_add_project(self):
        self.generate_user()
        self.assertEqual(self.freelancer.get_project("TestProject").get_name(), "TestProject")
        self.assertEqual(self.freelancer.get_project("TestProject").get_description(), "TDesc")

    def test_del_project(self):
        self.freelancer.add_project("TestDProject", "TDesc", "TDls",
                                    100, 20)
        self.freelancer.del_project("TestDProject")
        with self.assertRaises(ModuleNotFoundError):
            self.freelancer.get_project("TestDProject")

    def test_general_income(self):
        self.generate_user()
        self.freelancer.add_project("TestDProject", "TDesc", "TDls",
                                    200, 120)
        self.assertEqual(self.freelancer.get_general_income(), 300)

    def test_general_cost(self):
        self.generate_user()
        self.freelancer.add_project("TestDProject", "TDesc", "TDls",
                                    200, 120)

        self.assertEqual(self.freelancer.get_general_costs(), 140)


class TestProject(unittest.TestCase):
    def setUp(self):
        freelancer = project.Freelancer("TestUser", "")
        freelancer.add_project("TestProject", "TDesc", "TDls", 100, 20)
        self.project = freelancer.get_project("TestProject")

    def generate_task(self):
        self.project.add_task("TestTask", "TDesc")

    def test_add_task(self):
        self.generate_task()
        self.assertEqual(self.project.get_task("TestTask").get_name(), "TestTask")
        self.assertEqual(self.project.get_task("TestTask").get_description(), "TDesc")

    def test_del_task(self):
        self.generate_task()
        self.project.del_task("TestTask")
        with self.assertRaises(ModuleNotFoundError):
            self.project.get_task("TestTask")

    def test_get_task(self):
        self.generate_task()
        self.assertEqual(self.project.get_task("TestTask").get_name(), "TestTask")
        with self.assertRaises(ModuleNotFoundError):
            self.project.get_task("TestTask1")


if __name__ == '__main__':
    unittest.main()
