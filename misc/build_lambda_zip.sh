#!/bin/bash

build_zip_archive() {
  ARCHIVE_NAME=$1

  mkdir package

  echo "Installing dependencies into 'package' folder"
  python3 -m pip install --target ./package -r requirements.txt

#  chmod 755 package

  cd package
  zip -r ../$ARCHIVE_NAME.zip .

  cd ..
  zip -r $ARCHIVE_NAME.zip src

  unzip -l $ARCHIVE_NAME.zip

#  RELATIVE_ARTIFACT_PATH=$1
#  LAMBDA_NAME_AND_VERSION=$("${RELATIVE_ARTIFACT_PATH}"../../misc/extract_lambda_name_version.sh)
#
#  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
#  docker build -t "${LAMBDA_NAME_AND_VERSION}" .
#
#  echo "Saving the image ${LAMBDA_NAME_AND_VERSION}"
#  ARTIFACT_FOLDER="${RELATIVE_ARTIFACT_PATH}"target
#  echo "Artifact folder: $ARTIFACT_FOLDER"
#  mkdir -p ${ARTIFACT_FOLDER}
#  docker save "${LAMBDA_NAME_AND_VERSION}" > "${ARTIFACT_FOLDER}/${LAMBDA_NAME_AND_VERSION}".tar
#
#  ls -l $ARTIFACT_FOLDER
#  echo "Current folder: $(pwd)"
}

build() {
  echo "Running code quality tools"
  pylint --rcfile="./../.pylintrc" src/ test/

  echo "Running tests"
  python3 -m unittest

  build_zip_archive $1
}

main() {
  build $1
}

main "$@"; exit
