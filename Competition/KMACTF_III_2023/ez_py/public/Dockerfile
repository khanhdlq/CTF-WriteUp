FROM python:3.8-alpine
WORKDIR /app
COPY src/ .
RUN pip install -r requirements.txt
RUN echo "KMACTF{FAKE_FLAG}" > /flag_$(head -c 5 /dev/urandom | xxd -p).txt 
USER nobody 
CMD ["python", "app.py"]