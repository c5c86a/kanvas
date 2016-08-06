#!/bin/bash
#
# Installs dependencies, runs migrations if any, builds and runs the software

export ENV="DEBIAN_FRONTEND noninteractive"

export BEFORECOPY="apt-get update -qq && apt-get install -qqy \
		gcc build-essential \
		sqlite3 libjpeg-dev zlib1g-dev \
		python python-pip python2.7-dev python-imaging \
    `# phantomjs is a run-time dependency and its runtime dependencies are below (some of them might be compile-time dependencies)` \
    libfontconfig1-dev libfreetype6-dev libssl-dev libpng12-dev \
    `# for provisioning` \
    git keychain \
    	  --no-install-recommends && rm -rf /var/lib/apt/lists/* && \
    mkdir /site && \
    mkdir /site/data && \
    mkdir /site/data/db && \
    mkdir /site/data/media && \
    mkdir /site/project"

#separated with whitespace
export VOLUMES="/site/data"
export PWD="/site/project"
#separated with whitespace
export PORTS="9000"

export AFTERCOPY="pip install -q -r $PWD/requirements.txt"

export ENTRYPOINT="$PWD/entrypoint.sh"

