#!/bin/bash

# Import the Beeline library
. beeline.properties

# Verify if the table exists
function table_exists() {
  table_name="$1"
  query="SHOW TABLES LIKE '$table_name'"
  result=$(beeline -e "$query")
  if [ -n "$result" ]; then
    return 0
  else
    return 1
  fi
}

# Verify if a column exists in a table
function column_exists() {
  table_name="$1"
  column_name="$2"
  query="SELECT column_name FROM ${hiveconf:hive.metastore.database.default}.INFORMATION_SCHEMA.COLUMNS WHERE table_name = '$table_name' AND column_name = '$column_name'"
  result=$(beeline -e "$query")
  if [ -n "$result" ]; then
    return 0
  else
    return 1
  fi
}

# Main function
function main() {
  table_name="students"
  column_name="name"

  # Verify if the table exists
  if ! table_exists "$table_name"; then
    echo "Table $table_name does not exist."
    exit 1
  fi

  # Verify if the column exists
  if ! column_exists "$table_name" "$column_name"; then
    echo "Column $column_name does not exist in table $table_name."
    exit 1
  fi

  # Check for sample college names
  college_names="Stanford Harvard"
  for college_name in $college_names; do
    if ! echo "$college_name" | grep -q "$(beeline -e "SELECT name FROM colleges")"; then
      echo "Could not find college name '$college_name' in table colleges."
      exit 1
    fi
  done

  # Everything is good!
  echo "All checks passed."
}

main $@
