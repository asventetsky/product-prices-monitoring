#!/bin/bash

prepare_terragrunt_variables() {
  AWS_ACCOUNT=$1
  ENVIRONMENT=$2
  PLACEHOLDER=$3
  RELATIVE_PATH=$4

  PATH_TO_ENV_VARS="${RELATIVE_PATH}../../infrastructure/environments/${ENVIRONMENT}/env_vars.yaml"

  LAMBDA_NAME_AND_VERSION=$("${RELATIVE_PATH}"../../misc/extract_lambda_name_version.sh)
  REGION=$(awk -F '"' '{print $2;exit}' < $PATH_TO_ENV_VARS)
  IMAGE_URI="${AWS_ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/${LAMBDA_NAME_AND_VERSION}"
  IMAGE_URI_ESC=$(sed 's/[\/\.]/\\&/g' <<<"$IMAGE_URI")

  sed -i "s/<$PLACEHOLDER>/$IMAGE_URI_ESC/g" "$PATH_TO_ENV_VARS"

  cat $PATH_TO_ENV_VARS
}

main() {
  prepare_terragrunt_variables $1 $2 $3 $4
}

main "$@"; exit
