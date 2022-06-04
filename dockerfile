FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y

WORKDIR /usr/app/src/

COPY ./03-data-processing ./

RUN pip install -r /usr/app/src/requirements.txt

CMD [ "python3", "./solution/solution.py" ]
