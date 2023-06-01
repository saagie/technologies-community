FROM python:3.9-slim
ARG PYTHON_VERSION=3.9

RUN pip install --upgrade pip
RUN pip install numpy pandas transformers==4.16.2 pyarrow
RUN pip3 install torch torchvision torchaudio transformers==4.16.2
RUN pip install plotly dash==1.13.3 dash-bootstrap-components==0.13.1 Werkzeug==2.0.3

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl
COPY . /
WORKDIR /


EXPOSE 8080
CMD ["python", "./serve.py"]
