# FROM joyzoursky/python-chromedriver:latest
# RUN apt install wget
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i google-chrome-stable_current_amd64.deb
# WORKDIR /code
# COPY ./requirements.txt /code/requirements.txt
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# COPY . /code
# WORKDIR /code
# EXPOSE 8080:8080
# CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8080", "--loop=asyncio"]

FROM python:3.9 as builder

RUN python3 -m venv /app
RUN /app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /app/bin/pip install -Ur /mnt/requirements.txt

FROM python:3.9 as app

WORKDIR /app

COPY --from=builder /app /app
COPY . .

EXPOSE 9000

CMD /app/bin/uvicorn main:app --host=0.0.0.0 --port=9000 --loop=asyncio