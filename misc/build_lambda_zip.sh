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
}

build() {
  echo "Running code quality tools"
  pylint --rcfile="./.pylintrc" src/ test/

  echo "Running tests"
  python3 -m unittest

  build_zip_archive $1
}

main() {
  build $1
}

main "$@"; exit
