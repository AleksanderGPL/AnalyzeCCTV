FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN apt update && apt install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]