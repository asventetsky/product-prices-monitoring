#!/bin/bash

build_image() {
  DIRECTORY=$1
  FILE_NAME="{$DIRECTORY}lambda_spec.txt"

  # Parse the values using awk
  NAME=$(awk -F= '/^name=/ {print $2}' "$FILE_NAME")
  VERSION=$(awk -F= '/^version=/ {print $2}' "$FILE_NAME")
  LAMBDA_NAME_AND_VERSION="${NAME}:${VERSION}"

  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
  docker build -t "${LAMBDA_NAME_AND_VERSION}" -f "$DIRECTORY/Dockerfile" .

  echo "Saving the image ${LAMBDA_NAME_AND_VERSION}"
  mkdir -p target
  docker save "${LAMBDA_NAME_AND_VERSION}" > target/"${LAMBDA_NAME_AND_VERSION}".tar
}

build() {
  echo "Installing dependencies"
  (cd ${{ inputs.directory }} && python3 -m pip install -r requirements.txt)

  echo "Running code quality tools"
  pylint ${{ inputs.directory }}

  echo "Running tests"
  (cd ${{ inputs.directory }} && python3 -m unittest)

  build_image $1
}



main() {
  build $1
}

main "$@"; exit