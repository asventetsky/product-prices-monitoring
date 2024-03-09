#!/bin/bash

build_image() {
  FILE_NAME='lambda_spec.txt'

  # Parse the values using awk
  NAME=$(awk -F= '/^name=/ {print $2}' "$FILE_NAME")
  VERSION=$(awk -F= '/^version=/ {print $2}' "$FILE_NAME")
  LAMBDA_NAME_AND_VERSION="${NAME}:${VERSION}"

  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
  docker build -t "${LAMBDA_NAME_AND_VERSION}" .

  echo "Saving the image ${LAMBDA_NAME_AND_VERSION}"
  mkdir -p ../target
  docker save "${LAMBDA_NAME_AND_VERSION}" > ../target/"${LAMBDA_NAME_AND_VERSION}".tar
}

build() {
  echo "Installing dependencies"
  python3 -m pip install -r requirements.txt

  echo "Running code quality tools"
  pylint --rcfile=../.pylintrc ${DIRECTORY}

  echo "Running tests"
  python3 -m unittest

  build_image
}



main() {
  build $1
}

main "$@"; exit
