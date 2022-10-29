FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN apt update \
    && apt install -y build-essential libffi-dev libnacl-dev python3-dev \
    && python -m pip install -U pip setuptools \
    && pip install wheel \
    && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY mochina.py /app/
CMD ["python", "mochina.py"]
