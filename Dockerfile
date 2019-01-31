FROM docker.io/halotools/python-sdk:ubuntu-16.04_sdk-1.2.3_py-2.7

WORKDIR /src/

COPY . /src/

RUN pip install -r requirements.txt

CMD python ./application.py
