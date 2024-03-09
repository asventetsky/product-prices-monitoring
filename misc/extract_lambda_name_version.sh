#!/bin/bash

extract_lambda_name_version() {
  FILE_NAME='lambda_spec.txt'

  # Parse the values using awk
  NAME=$(awk -F= '/^name=/ {print $2}' "$FILE_NAME")
  VERSION=$(awk -F= '/^version=/ {print $2}' "$FILE_NAME")
  LAMBDA_NAME_AND_VERSION="${NAME}:${VERSION}"

  echo $LAMBDA_NAME_AND_VERSION
}

main() {
  echo $(extract_lambda_name_version)
}

main "$@"; exit
