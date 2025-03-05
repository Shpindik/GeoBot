FROM python:3.12

WORKDIR /bot

COPY bot/ bot/
COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
