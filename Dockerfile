FROM debian:stretch

ENV PYTHONUNBUFFERED=1 \
	DEBIAN_FRONTEND=noninteractive

RUN \
	echo "Install base packages" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		make \
		git \
		gnupg \
		python2.7 \
		python3.5 \
		python3-pip \
		python3-setuptools \
		python-pip \
		python-setuptools \
	&& echo "Clean up" \
	&& rm -rf /tmp/*

RUN \
	echo "Install global pip packages" \
	&& python3.5 -m pip install tox

WORKDIR /var/project
