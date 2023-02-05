FROM docker.io/library/python:3.10

WORKDIR /src

RUN useradd -m -r user && chown user /src

COPY . .

RUN apt install imagemagick

USER user

RUN pip install -r /src/requirements.txt


CMD ["python", "./main.py"]
