FROM python:3.7-alpine
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#
#COPY . main_office/

CMD ["uvicorn", "main_office.main:app", "--reload", "--host", "0.0.0.0"]