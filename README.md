# fastapi

# .env 
VK_ACCESS_TOKEN=
OUTPUT_DIRECTORY= "/your/path/pdf"
CELERY_BROKER_URL='redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/0'
SQLALCHEMY_DATABASE_URL="postgresql://user_name:password@host:5433/db_name"

убедитесь, что у вас есть ключи API ВК

# Запуск проекта локально

клонировать репозиторий

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
cd fastapi
```

```bash
pip install -r requirements.txt
```
```bash
 uvicorn app.main:app --reload
```

#celery

```bash
celery -A app.worker.celery worker --loglevel=info
```



## License

[MIT](https://choosealicense.com/licenses/mit/)