FROM python:latest

RUN mkdir -p /reading

WORKDIR /src

COPY ./src/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py"]