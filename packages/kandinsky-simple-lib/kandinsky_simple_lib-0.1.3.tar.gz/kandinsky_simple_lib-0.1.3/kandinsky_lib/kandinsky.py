import json
import time
import requests
import base64
from io import BytesIO
from PIL import Image

class KandinskyAPI:
    def __init__(self, api_key, secret_key, url):
        """
        Инициализация API-клиента Kandinsky.

        Параметры:
            api_key (str): API ключ пользователя.
            secret_key (str): Секретный ключ пользователя.
            url (str): Базовый URL API. По умолчанию — для сервиса FusionBrain.
        """
        self.url = url
        self.headers = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}'
        }

    def get_model(self):
        """
        Получает ID доступной модели.

        Возвращает:
            str: ID модели.
        """
        response = requests.get(self.url + 'key/api/v1/models', headers=self.headers)
        response.raise_for_status()  # Проверка статуса ответа
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        """
        Генерация изображения по текстовому запросу.

        Параметры:
            prompt (str): Описание изображения.
            model (str): ID модели для генерации.
            images (int): Количество изображений для генерации.
            width (int): Ширина изображения.
            height (int): Высота изображения.

        Возвращает:
            str: UUID запроса генерации.
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.url + 'key/api/v1/text2image/run', headers=self.headers, files=data)
        response.raise_for_status()
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        """
        Проверяет статус генерации изображения.

        Параметры:
            request_id (str): UUID запроса генерации.
            attempts (int): Количество попыток проверки.
            delay (int): Задержка между проверками.

        Возвращает:
            list: Список изображений в формате Base64 при успешной генерации или None.
        """
        while attempts > 0:
            response = requests.get(self.url + f'key/api/v1/text2image/status/{request_id}', headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)
        return None

    def save_image(self, image_data, filename="generated_image.png"):
        """
        Сохраняет изображение на устройство.

        Параметры:
            image_data (str): Изображение в формате Base64.
            filename (str): Имя файла для сохранения.
        """
        img_data = base64.b64decode(image_data)
        image = Image.open(BytesIO(img_data))
        image.save(filename)
        print(f"Изображение сохранено как {filename}")
