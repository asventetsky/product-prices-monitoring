#!/bin/bash

build_zip_archive() {
  ARCHIVE_NAME=$1

  if test -f requirements.txt; then
    echo "Creating zip archive WITH dependencies"
    mkdir package

    echo "Installing dependencies into 'package' folder"
    python3 -m pip install --target ./package -r requirements.txt

    #  chmod 755 package

    echo "Listing 'package' folder"
    ls -l package

    cd package
    zip -qr ../$ARCHIVE_NAME.zip .

    cd ..
    zip -r $ARCHIVE_NAME.zip src
  else
    echo "Creating zip archive WITHOUT dependencies"
    zip -r $ARCHIVE_NAME.zip src
  fi

  echo "Listing archive content"
  unzip -l $ARCHIVE_NAME.zip

  mv $ARCHIVE_NAME.zip ./../target
  ls -l ./../target
}

build() {
  echo "Running code quality tools"
#  pylint --rcfile="./.pylintrc" src/ test/

  echo "Running tests"
  python3 -m unittest

  echo "Building zip archive"
  build_zip_archive $1
}

main() {
  build $1
}

main "$@"; exit
