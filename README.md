
![ - a  r  g  e  n  t  o - ](images/argento.png)

## ARGENTO - docker app агент с админкой. 
### Django-приложение для Retrieval-Augmented Generation с использованием Ollama или SDK (Pinecone, ChatGPT).

> [!NOTE]
> Приложение в процессе разработки.


---

Это Django-приложение реализует возможность легкого развертывания чат бота с RAG (Retrieval-Augmented Generation) для выполнения бизнес задач. 

#### Сценарий использования:
- Через админ панель загружается документация (текст или PDF).
- Документация переобразуется в векрторы для RAG (Vector Storage на борту) или SDK например Pinecone.
- При необходимости при помощи утилиты `Django Commands` запускаем телеграм бот TelegramBotAPI. Бот диаложит в контексте бизнес задачи. Инструктирует, консультирует, вызывает function tools...
- Создаем ендпоинты для работы с конкретной тематикой\топиком на случай если нужно подобное (например для веб сайта).
- Ендпоинт возвращает сгенерированные ответы моделью в обученом контексте.
- Настроить Function Tools который может выполнять задачи (например высылать документы, делать заказы, формировать подборки товаров).
- В админке есть выгрузка таблиц по клиентам\диалогам и статистика.
* возможно что то добавится или изменится.


---


### Запуск

- клонируем репозиторий `git@github.com:ivanIStereotekk/bot-station.git`
- переименовывваем файл с переменными окружения из ` .env_example ` в ` .env `
- запускаем в директории с проектом ` docker compose up `

---

<!-- ####  текущее состояние:

- скрипт entrypoint.sh автоматически создает superuser, миграции, и запускает бота.

- на сайте администратора имеется возможность импорта/экспорта exel файлов с данными  

- по группам, по фильтрам, по датам, все вместе...

- данные для входа в админку в .env файле `DJANGO_SUPERUSER_NAME` `DJANGO_SUPERUSER_PASS`

- OpenAI SDK - генерация текста на базе чатов/ботов в Telegram

- Faiss vector store


--- -->



#### URL с параметрами для `POST` запроса

> [!NOTE]
> URL должен соответствовать вашему домену или имени хоста в docker.

 ```http://localhost:8000/send_user_query_data/?name=Jichael%20Mackson&email=juchael.mackson%40gmail.com&phone=%+79883442299&comment=Jichael_Mackson%&topic=Helloworld&contact=Мои&Контакты```




## Если хотим запуститься локально DEBUG (Local Setup):

Создаем в рабочей директории .env файл (референс .env_example)

- Устанавливаем при помощи Pyenv версию интерпритатора (Python 3.11) для проекта.
- Создаем окружение `pyenv virtualenv 3.11 argento_venv`
- Активируем окружение `pyenv activate argento_venv`
- Устанвливаем зависимости `pip install -r requirements.txt`
- Создаем миграции `python manage.py makemigrations`
- Пишем миграции в БД `python manage.py migrate`
- Создаем автоматически (Django Commands) суперюзера для доступа к админке `python manage.py superuser_create` (Не забыть указать нужные параметры в файле .env)
- Или можем создать суперюзера стандартным методом `python manage.py createsuperuser` отвечаем на вопросы...

<!-- Можем создать скрипт sh с теми же командами:

```bash
#!/bin/sh

pyenv virtualenv 3.11 argento_venv

pyenv activate argento_venv

pip install -r requirements.txt

cd ./botlog

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py superuser_create


python manage.py runserver 0.0.0.0:8000 & python manage.py bot_notify

# exit

``` -->


---

## Установка Ollama:

> [!NOTE]
> Ollama is the easiest way to get up and running with large language models such as gpt-oss, Gemma 3, DeepSeek-R1, Qwen3 and more.
> Ollama guide Linux- https://docs.ollama.com/linux



- Устанавливаем - `curl -fsSL https://ollama.com/install.sh | sh`

- Запускаем модель (например Llama3.2) - `ollama run llama3.2`

---

## Вариант RAG 

---

- Скачиваем модель для эмбедингов - `ollama pull all-minilm` - (выбираем нужную модель) 

#### Example embedding models - Модели для эмбедингов
Model	Parameter Size	
mxbai-embed-large	334M	
nomic-embed-text	137M
all-minilm          23M

---

#### Подробнее - `https://ollama.com/blog/embedding-models`

---
##### Пример генерации текста в контектсе pdf документа ( сохранил для теста пдф страницу со своего сайта\блога ).

```
Enter Question: 
- Расскажи о ком речь в документе  ?
- Приветствую! 
В этом документе есть запись от автора о том, что он по-прежнему является в поиске вакансии и хочет найти коллектив с кем будет комфортно работать. Он также пишет о том, что для него важно иметь позитивные люди вокруг, а когда занятие в радость, все складывается хорошо.

Из этой записи следует, что этот человек по-прежнему ищет постоянное место работы.
Enter Question: ...

```