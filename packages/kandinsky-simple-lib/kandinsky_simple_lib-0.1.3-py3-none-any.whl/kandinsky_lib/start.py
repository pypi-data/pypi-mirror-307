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