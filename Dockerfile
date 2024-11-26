FROM debian:buster

ENV PYTHONUNBUFFERED=1 \
	DEBIAN_FRONTEND=noninteractive

RUN \
	echo "Install base packages" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		awscli \
		gcc \
		git \
		gnupg \
		curl \
		ca-certificates \
		jq \
		# pyenv dependencies (https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
		make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
		libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev \
		libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
	&& echo "Clean up" \
	&& rm -rf /tmp/*

RUN \
	echo "install pyenv" \
	&& curl https://pyenv.run | bash

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN ls /root/.pyenv/bin
RUN eval "$(/root/.pyenv/bin/pyenv init - )"

WORKDIR /var/project

COPY tox-python-versions .

RUN \
	echo "Install python based on tox-python-versions file" \
	&& xargs -a tox-python-versions -n 1 -P $(nproc) pyenv install

COPY . .

# Make pyenv activate all installed Python versions for tox (available as pythonX.Y)
# The first version in the file will be the one used when running "python"
RUN pyenv global $(tr '\n' ' ' < tox-python-versions)

RUN make bootstrap

RUN \
	echo "installing tox" \
	&& pip install tox
