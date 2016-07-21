FROM python:2.7-slim
LABEL "purpose"="clean environment for webapp development"

# workaround for apt-get
ENV DEBIAN_FRONTEND noninteractive

# having a requirements.txt would mean rerunning apt-get as docker cannot reuse apt-get when it is after VOLUME
RUN apt-get update -qq && apt-get install -qqy \
		gcc build-essential \
		sqlite3 libjpeg-dev zlib1g-dev \
		python python-pip python2.7-dev python-imaging \
    `# phantomjs is a run-time dependency and its runtime dependencies are below (some of them might be compile-time dependencies)` \
    libfontconfig1-dev libfreetype6-dev libssl-dev libpng12-dev \
    	  --no-install-recommends && rm -rf /var/lib/apt/lists/* 

RUN mkdir /site
RUN mkdir /site/data
RUN mkdir /site/data/db
RUN mkdir /site/data/media
RUN mkdir /site/project
VOLUME ["/site/data"]
COPY . /site/project
WORKDIR /site/project
EXPOSE 8000

RUN pip install -q -r requirements.txt

ENTRYPOINT ["/site/project/entrypoint.sh"]

