FROM python:3.11.0

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD [ "python", "index.py" ]
