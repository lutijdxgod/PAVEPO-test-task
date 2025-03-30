# Руководство по запуску приложения

Убедитесь, что у вас установлен Docker Desktop.

1. **Создайте новое приложение на сайте Yandex ID:**
   - Перейдите по ссылке: [https://oauth.yandex.ru/client/new/id](https://oauth.yandex.ru/client/new/id)
   - Выберите "Web-services" для вашей платформы.
   - В поле "Redirect URI" укажите `http://localhost:8000/auth/callback`.

2. **Клонируйте этот репозиторий.**

3. **Создайте файл `.env` и заполните его данными:**
   - Скопируйте структуру из файла `.env.example`.
   - Не забудьте добавить информацию Yandex ID, полученную на предыдущем шаге: `client_id` и `client_secret`.

4. **Создайте файл `alembic.ini` и заполните его данными:**
   - Скопируйте структуру из файла `alembic.ini.example`.
   - Убедитесь, что все параметры соответствуют вашей среде.

5. **Убедитесь, что Docker Desktop запущен.**

6. **Запустите приложение с помощью Docker Compose:**
   - Выполните команду:
     ```bash
     docker-compose up --build
     ```
   - Эта команда соберет образы и запустит контейнеры приложения.

Следуя этим инструкциям, вы сможете успешно запустить приложение на вашей машине.
