#!/bin/bash

push_image() {
  AWS_ACCOUNT=$1
  AWS_REGION=$2
  RELATIVE_PATH=$3

  ECR_ACCOUNT="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
  LAMBDA_NAME_AND_VERSION=$("${RELATIVE_PATH}"../../misc/extract_lambda_name_version.sh)

  echo "Loading the image ${LAMBDA_NAME_AND_VERSION}"
  docker load --input ../target/"${LAMBDA_NAME_AND_VERSION}".tar

  echo "Tagging the image ${LAMBDA_NAME_AND_VERSION} with ${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
  sudo docker tag "${LAMBDA_NAME_AND_VERSION}" "${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"

  echo "Logging to $ECR_ACCOUNT"
  aws ecr get-login-password --region $AWS_REGION | sudo docker login --username AWS --password-stdin $ECR_ACCOUNT || exit
  echo "Pushing image to ${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
  sudo docker push "${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
}

main() {
  push_image $1 $2 $3
}

main "$@"; exit
