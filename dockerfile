FROM python:latest

WORKDIR /usr/app/src/

COPY ./03-data-processing ./

RUN pip install -r /usr/app/src/requirements.txt

CMD [ "python3", "solution/solution.py" ]
