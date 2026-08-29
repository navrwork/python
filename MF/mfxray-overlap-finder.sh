#!/bin/bash

# Define funds and their short labels (no spaces)
declare -A labels=(
  ["hdfc-nifty-50-index-fund"]="HDFC_N50"
  ["hdfc-nifty50-equal-weight-index-fund"]="HDFC_N50EW"
  ["hdfc-nifty-100-equal-weight-index-fund"]="HDFC_N100EW"
  ["hdfc-flexi-cap-fund"]="HDFC_Flexi"
  ["parag-parikh-flexi-cap-fund"]="PP_Flexi"
  ["icici-prudential-flexicap-fund"]="ICICI_Flexi"
  ["icici-prudential-multi-asset-fund"]="ICICI_MultiAst"
  ["icici-prudential-nifty-midcap-150-index-fund"]="ICICI_Mid150"
  ["hdfc-small-cap-fund"]="HDFC_SmallCap"
)

funds=(
  "hdfc-nifty-50-index-fund"
  "hdfc-nifty50-equal-weight-index-fund"
  "hdfc-nifty-100-equal-weight-index-fund"
  "hdfc-flexi-cap-fund"
  "parag-parikh-flexi-cap-fund"
  "icici-prudential-flexicap-fund"
  "icici-prudential-multi-asset-fund"
  "icici-prudential-nifty-midcap-150-index-fund"
  "hdfc-small-cap-fund"
)

# Print header row (comma-separated)
echo -n "Fund"
for f in "${funds[@]}"; do
  echo -n ",${labels[$f]}"
done
echo

# Loop rows
for a in "${funds[@]}"; do
  echo -n "${labels[$a]}"
  for b in "${funds[@]}"; do
    if [ "$a" == "$b" ]; then
      echo -n ",100"
    else
      pct=$(curl -s "https://mfxray.in/api/quick-compare?a=$a&b=$b" \
        --compressed \
        -H "Accept: application/json" \
        -H "User-Agent: Mozilla/5.0" \
        -H "Referer: https://mfxray.in/compare" \
        | jq -r '.overlap_pct')
      echo -n ",$pct"
    fi
  done
  echo
done
