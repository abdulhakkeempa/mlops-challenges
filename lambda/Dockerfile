FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install ultralytics --no-deps
RUN pip3 install opencv-python-headless
RUN pip3 install numpy

RUN pip install -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]