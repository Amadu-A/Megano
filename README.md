# install pre-commit
    create - .pre-commit-config.yaml
    pip install pre-commit
    pre-commit install(устанавливаем нашу настройку)

# desk for draw
    https://drive.google.com/file/d/1o4hx971-LXY4lLG7rHLLGDCOtVnwPLnE/view?usp=sharing

# file for url
    https://docs.google.com/spreadsheets/d/1ik2Ef-MiPBZU5R-QrMDTuIXscI4pdtK9NOXPPrgQtr8/edit?usp=sharing

# trello
    https://trello.com/b/6rt99RrV/pythondjangoteam29

# rule for commit
    origin/fixbugs/задача или номер задачи
    origin/feature/задача или номер задачи

# rule for dump data
    python fixtures_dumper.py

# rule for load data
    python manage.py migrate
    python manage.py import_fixtures (-f filename -e email (не обязательные аргументы))

# running Celery
    pip install -r requirements.txt
    celery -A shope worker --loglevel=info

# Running docker
    docker compose up -d --build - сборка перед стартом контейнеров
    docker compose up -d - запуск контейнеров (-d для запуска в фоне)
    docker compose down - остановка контейнеров

# Admin
    admin@mail.ru (почта)
    admin    (пароль)

# Add permissions for sellers
    python manage.py seller_permissions

# Add tags to products
    python manage.py add_tags_to_product_cards
