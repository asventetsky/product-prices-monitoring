#!/bin/bash

build_image() {
  RELATIVE_ARTIFACT_PATH=$1
  LAMBDA_NAME_AND_VERSION=$("${RELATIVE_ARTIFACT_PATH}"../../misc/extract_lambda_name_version.sh)

  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
  docker build -t "${LAMBDA_NAME_AND_VERSION}" .

  echo "Saving the image ${LAMBDA_NAME_AND_VERSION}"
  ARTIFACT_FOLDER="${RELATIVE_ARTIFACT_PATH}"target
  echo "Artifact folder: $ARTIFACT_FOLDER"
  mkdir -p ${ARTIFACT_FOLDER}
  docker save "${LAMBDA_NAME_AND_VERSION}" > "${ARTIFACT_FOLDER}/${LAMBDA_NAME_AND_VERSION}".tar

  ls -l $ARTIFACT_FOLDER
  echo "Current folder: $(pwd)"
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
