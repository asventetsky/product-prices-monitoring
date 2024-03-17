#!/bin/bash

adjust_price_format_for_historic_prices() {
  SOURCE_TABLE="product_prices"
  DESTINATION_TABLE="historic_product_prices"

  aws dynamodb scan --table-name ${SOURCE_TABLE} --output json > data.json

  original_json=$(<data.json)

  # Modify the date field
  modified_json=$(jq '.Items[].date.S |= sub("(?<day>[0-9]{2})-(?<month>[0-9]{2})-(?<year>[0-9]{4})"; "\(.year)-\(.month)-\(.day)")' <<< "$original_json")

  # Extract items from the original JSON
  items=$(jq '.Items' <<< "$modified_json")

  # Wrap each item in a PutRequest object and enclose them in a DESTINATION_TABLE name
  modified_json="{ \"${DESTINATION_TABLE}\": [ $(jq -c '.[] | {PutRequest: {Item: .}}' <<< "$items" | paste -sd ',' -) ] }"

  echo "$modified_json" > formatted.json

  aws dynamodb batch-write-item --request-items file://formatted.json

  rm data.json
  rm formatted.json
}

main() {
  adjust_price_format_for_historic_prices
}

main "$@"; exit
