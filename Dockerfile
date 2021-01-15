FROM python:3.7

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt