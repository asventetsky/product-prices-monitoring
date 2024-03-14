#!/bin/bash

increment_patch_version() {
  FILE_NAME='lambda_spec.txt'

  CURRENT_VERSION=$(awk -F= '/^version=/ {print $2}' "$FILE_NAME")

  MAJOR_MINOR=$(echo "$CURRENT_VERSION" | cut -d'.' -f1-2)

  PATCH=$(echo "$CURRENT_VERSION" | cut -d'.' -f3 | cut -d'-' -f1)
  SUFFIX=$(echo "$CURRENT_VERSION" | cut -d'-' -f2-)

#  PATCH_SUFFIX=$(echo "$CURRENT_VERSION" | cut -d'.' -f3)
#  PATCH=$(echo "$PATCH_SUFFIX" | cut -d'-' -f1)
#  SUFFIX=$(echo "$PATCH_SUFFIX" | cut -d'-' -f2-)

  ((PATCH++))

  NEW_VERSION="$MAJOR_MINOR.$PATCH-$SUFFIX"

  sed -i "s/^version=.*/version=$NEW_VERSION/" "$FILE_NAME"

  echo "New version: $NEW_VERSION"
}

main() {
  increment_patch_version
}

main "$@"; exit
