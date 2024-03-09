#!/bin/bash

push_image() {
  AWS_ACCOUNT=$1
  AWS_REGION=$2
  echo "AWS_ACCOUNT=${AWS_ACCOUNT}, AWS_REGION=${AWS_REGION}"

  ECR_ACCOUNT="${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

  FILE_NAME="lambda_spec.txt"

  # Parse the values using awk
  NAME=$(awk -F= '/^name=/ {print $2}' "$FILE_NAME")
  VERSION=$(awk -F= '/^version=/ {print $2}' "$FILE_NAME")
  LAMBDA_NAME_AND_VERSION="${NAME}:${VERSION}"

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
