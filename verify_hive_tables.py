# Verify if a table exists
def table_exists(table_name):
  """
  Verify if a table exists in Hive.

  Args:
    table_name: The name of the table to check.

  Returns:
    True if the table exists, False otherwise.
  """

  query = "SHOW TABLES LIKE '{}'".format(table_name)
  result = hive.query(query)
  if result:
    return True
  else:
    assert False, "Table {} does not exist.".format(table_name)

# Verify if a column exists in a table
def column_exists(table_name, column_name):
  """
  Verify if a column exists in a table in Hive.

  Args:
    table_name: The name of the table to check.
    column_name: The name of the column to check.

  Returns:
    True if the column exists, False otherwise.
  """

  query = """
    SELECT column_name
    FROM
      ${hiveconf:hive.metastore.database.default}.INFORMATION_SCHEMA.COLUMNS
    WHERE
      table_name = '{}'
      AND column_name = '{}'
  """.format(table_name, column_name)
  result = hive.query(query)
  if result:
    return True
  else:
    assert False, "Column {} does not exist in table {}.".format(column_name, table_name)

# Main function
def main():
  """
  The main function.
  """

  table_name = "students"
  column_name = "name"

  # Verify if the table exists
  assert table_exists(table_name)

  # Verify if the column exists
  assert column_exists(table_name, column_name)

  # Check for sample college names
  assert "Stanford" in hive.query("SELECT name FROM colleges")
  assert "Harvard" in hive.query("SELECT name FROM colleges")

if __name__ == "__main__":
  main()
