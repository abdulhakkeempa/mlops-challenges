FROM python:3.11-slim

WORKDIR /code

COPY ./req.txt /code/req.txt

RUN pip3 install --upgrade pip

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install ultralytics --no-deps
RUN pip3 install opencv-python-headless
RUN pip3 install --no-cache-dir --upgrade -r /code/req.txt

COPY main.py /code/
COPY models /code/models

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

