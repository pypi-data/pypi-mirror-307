import unittest
from kandinsky_lib.kandinsky import KandinskyAPI

class TestKandinskyAPI(unittest.TestCase):
    
    def setUp(self):
        # Здесь вы можете инициализировать объекты перед тестами
        self.api_key = "80286D572B0C18AE90A4F84C4FB2FF81"
        self.secret_key = "9C40008A6BDEA87F1EDA831600241AA3"
        self.api = KandinskyAPI(self.api_key, self.secret_key)

    def test_model_id(self):
        # Пример теста
        model_id = self.api.get_model()
        self.assertIsNotNone(model_id, "Model ID should not be None")

    def test_generate_image(self):
        # Пример теста
        prompt = "A beautiful sunset"
        uuid = self.api.generate(prompt, "model_id")
        self.assertIsNotNone(uuid, "UUID should not be None")

if __name__ == "__main__":
    unittest.main()
