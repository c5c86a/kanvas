#!/bin/bash
#
# Installs dependencies, runs migrations if any, builds and runs the software

arg=`cat $ENV | sed 's/ /=/g'`
export $arg

sudo $BEFORECOPY
sudo $AFTERCOPY

$ENTRYPOINT

