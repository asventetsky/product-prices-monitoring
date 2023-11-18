#!/bin/bash

build_and_push_images() {
  AWS_ACCOUNT=$1
  AWS_REGION=$2

  ECR_ACCOUNT="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

  LAMBDA_SPEC=($(cat lambda_spec.txt | tr "=" " "))
  LAMBDA_NAME_AND_VERSION=${LAMBDA_SPEC[0]}
  echo "LAMBDA_NAME_AND_VERSION=${LAMBDA_NAME_AND_VERSION}"

  echo "Building the image ${LAMBDA_NAME_AND_VERSION}"
  sudo docker build -t "${LAMBDA_NAME_AND_VERSION}" .
  echo "Tagging the image ${LAMBDA_NAME_AND_VERSION} with ${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
  sudo docker tag "${LAMBDA_NAME_AND_VERSION}" "${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"

  echo "Logging to $ECR_ACCOUNT"
  aws ecr get-login-password --region $AWS_REGION | sudo docker login --username AWS --password-stdin $ECR_ACCOUNT || exit
  echo "Pushing image to ${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
  sudo docker push "${ECR_ACCOUNT}/${LAMBDA_NAME_AND_VERSION}"
}

main() {
  build_and_push_images $1 $2
}

main "$@"; exit
