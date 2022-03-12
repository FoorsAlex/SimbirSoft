FROM python:3.7-slim
RUN mkdir /code
COPY . /code
WORKDIR /code
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
CMD ["gunicorn", "simbir_note.wsgi:application", "--bind", "0:8000" ]
