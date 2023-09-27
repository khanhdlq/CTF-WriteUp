FROM python:slim-buster

RUN apt update -y && apt install libmagic1 -y

RUN python -m pip install --upgrade pip

RUN pip3 install flask requests python-magic

WORKDIR /app

COPY ./src .

COPY /flag.txt /

COPY /make_color.sh /

RUN chmod +x /make_color.sh && /make_color.sh && rm -f /make_color.sh

EXPOSE 9000

CMD python app.py

