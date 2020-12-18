FROM python:3.7-alpine
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . filia/

RUN ls -la
RUN pwd
RUN ls -la filia

CMD ["uvicorn", "filia.main:app", "--reload",  "--host", "0.0.0.0"]