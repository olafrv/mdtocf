# docker build -t md2cf .
# docker run --rm -it md2cf -h

FROM ubuntu:18.04 AS stage1
RUN apt update \
    && apt install -y virtualenv python3.7 python-pip \
    && apt clean -y

FROM stage1 as stage2
COPY requirements.txt /tmp/ 
WORKDIR /md2cf
RUN virtualenv --python=python3.7 venv \
    && chmod +x venv/bin/activate \
    && . venv/bin/activate \
    && python -m pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

FROM stage2
COPY . /md2cf
WORKDIR /md2cf
RUN chmod +x run.sh

ENTRYPOINT [ "/md2cf/run.sh" ]
CMD [ "-c" ]
