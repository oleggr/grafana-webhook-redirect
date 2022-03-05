FROM joyzoursky/python-chromedriver:latest
RUN apt install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
WORKDIR /code
EXPOSE 8080:8080
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8080", "--loop=asyncio"]