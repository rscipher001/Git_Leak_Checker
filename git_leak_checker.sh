#!/bin/bash

# List of User Agents
UA[0]="Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0"
UA[1]="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
UA[2]="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
UA[3]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

# Size of UA Array
size=${#UA[@]}

# Global Variables
filename="$1"
output="out.txt"
progress=0
success=0
final_progress=$(wc -l $1 | cut -f1 -d' ')

check_git_leak () {
  # Choose random UA
  index=$(($RANDOM % $size))

  # Make cURL request
  response=$(curl -L -s -A ${UA[$index]} \
  -H 'Accept-Encoding: identity' \
  -H 'Connection: close' \
  $1/.git/HEAD)

  # Check response
  if [[ $response == "ref: refs"* ]]; then
    success=$(($success+1))
    echo $1 >> $output
  fi
}

# Read URLs and try
while read -r url; do
  check_git_leak $url
  echo -ne "Progress: $progress/$final_progress, Success: $success\r"
  progress=$(($progress+1))
done < "$filename"
