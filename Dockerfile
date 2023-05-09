FROM python:3.10-slim

# Установка необходимых пакетов для запуска cron
RUN apt-get update && apt-get install -y cron

# Копирование проекта в контейнер
COPY . /bot_cron

# Установка зависимостей из requirements.txt
RUN pip install -r /bot_cron/requirements.txt

# Добавление задания в cron для запуска скрипта два раза в день
RUN echo "* 10 * * * cd /bot_cron && python3 get_price_for_html.py" >> /etc/crontab
RUN echo "* 18 * * * cd /bot_cron && python3 get_price_for_html.py" >> /etc/crontab

# Запуск cron и бесконечного цикла для поддержания контейнера в работе
CMD service cron start && tail -f /dev/null