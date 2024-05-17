FROM python:3.10

WORKDIR /app

COPY . ./app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV HOST=192.168.5.191

RUN chmod +x start.sh

CMD ["./start.sh"]
