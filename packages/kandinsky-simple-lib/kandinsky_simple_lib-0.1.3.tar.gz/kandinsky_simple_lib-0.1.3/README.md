# kandinsky-simple-lib

`kandinsky-simple-lib` — это простая библиотека для создания изображений с помощью API Kandinsky. Она позволяет генерировать изображения на основе текстовых описаний, взаимодействуя с API, и сохранять их на вашем устройстве.

## Установка

Для использования библиотеки, сначала установите её с помощью `pip`:

```bash
pip install kandinsky-simple-lib
```

примеры

```
from kandinsky_lib import KandinskyAPI
def main():
    # Замените на ваш API ключ и секретный ключ
    api_key = "your api key"
    secret_key = "your secret key"
    url = "https://api-key.fusionbrain.ai/"
    # Описание изображения для генерации
    prompt = "A beautiful sunset over the ocean"

    # Создаем объект API с вашими ключами
    api = KandinskyAPI(api_key, secret_key, url)

    # Получаем ID доступной модели
    model_id = api.get_model()

    # Генерируем изображение
    uuid = api.generate(prompt, model_id)

    # Проверяем статус генерации и получаем изображения
    images = api.check_generation(uuid)

    if images:
        # Сохраняем изображение на устройство
        api.save_image(images[0], "generated_image.png")
        print("Изображение успешно сохранено как 'generated_image.png'.")
    else:
        print("Не удалось сгенерировать изображение.")

if __name__ == "__main__":
    main()
```

Описание параметров:
api_key: Ваш API ключ.
secret_key: Ваш секретный ключ.
prompt: Текстовое описание того, что вы хотите, чтобы нейросеть сгенерировала. Например: "A beautiful sunset over the ocean".
Описание методов:
get_model(): Получает ID доступной модели для генерации изображений.
generate(prompt, model): Генерирует изображение на основе текстового описания.
check_generation(request_id): Проверяет статус генерации изображения.
save_image(image_data, filename): Сохраняет изображение в файл.
