FROM python:latest

WORKDIR /src

COPY ./src/* ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "main.py"]