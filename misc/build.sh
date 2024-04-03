#!/bin/bash

build_image() {
  ARTEFACT_FOLDER=$1
  LAMBDA_NAME_AND_VERSION=$("${ARTEFACT_FOLDER}"/../../misc/extract_lambda_name_version.sh)
#  LAMBDA_NAME_AND_VERSION=$(./../../../../misc/extract_lambda_name_version.sh)

  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
  docker build -t "${LAMBDA_NAME_AND_VERSION}" .

  echo "Saving the image ${LAMBDA_NAME_AND_VERSION}"
  mkdir -p $ARTEFACT_FOLDER
  docker save "${LAMBDA_NAME_AND_VERSION}" > "${ARTEFACT_FOLDER}"/"${LAMBDA_NAME_AND_VERSION}".tar
}

build() {
  echo "Installing dependencies"
  python3 -m pip install -r requirements.txt

  echo "Running code quality tools"
  pylint --rcfile="./../.pylintrc" src/ test/

  echo "Running tests"
  python3 -m unittest

  build_image $1
}

main() {
  build $1
}

main "$@"; exit
