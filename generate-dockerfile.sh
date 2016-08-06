#!/bin/bash
#

echo "FROM python:2.7-slim
LABEL 'purpose'='clean environment for webapp development'
ENV $ENV

RUN $BEFORECOPY

VOLUME [$VOLUMES]
COPY . $COPY
EXPOSE $PORTS

RUN $AFTERCOPY

ENTRYPOINT ['$ENTRYPOINT']" > Dock

