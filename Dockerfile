# Execute: `make docker`

FROM ubuntu:18.04 AS stage1
RUN apt update \
    && apt install -y virtualenv python3.7 python-pip \
    && apt clean -y

FROM stage1 as stage2
COPY requirements.txt /tmp/ 
WORKDIR /mdtocf
RUN virtualenv --python=python3.7 venv \
    && chmod +x venv/bin/activate \
    && . venv/bin/activate \
    && python -m pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

FROM stage2
COPY . /mdtocf

ENTRYPOINT [ "/mdtocf/venv/bin/python" , "-m", "mdtocf.mdtocf" ]
CMD [ "-c" ]
