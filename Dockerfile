FROM python:3.10
WORKDIR /app

COPY main.py /app
COPY main-discord.py /app
COPY main-revolt.py /app
COPY .env.example /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

CMD ["python", "./main.py"]