DOCKER_IMAGE_NAME=notifications-python-client

docker run \
  --rm \
  -v "`pwd`:/var/project" \
  -v "`pwd`/tox-python-versions:/var/project/.python-version" \
  --env-file docker.env \
  -it \
  ${DOCKER_IMAGE_NAME} \
  ${@}
