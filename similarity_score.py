import pandas as pd
import fuzzywuzzy

def preprocess_column_name(column_name):
  """
  Preprocesses a column name by converting it to lowercase, removing punctuation, and splitting camel case column names into individual words.

  Args:
    column_name: The column name to preprocess.

  Returns:
    A preprocessed column name.
  """

  column_name = column_name.lower()
  column_name = column_name.replace('_', ' ')
  column_name = column_name.split()

  return column_name

def create_short_form_dictionary():
  """
  Creates a dictionary of common short forms and their full names.

  Returns:
    A dictionary of common short forms and their full names.
  """

  short_form_dictionary = {}
  short_form_dictionary['ctry_cd'] = 'country_code'
  short_form_dictionary['state_cd'] = 'state_code'
  short_form_dictionary['zip_cd'] = 'zip_code'
  short_form_dictionary['cust_id'] = 'customer_id'
  short_form_dictionary['prod_id'] = 'product_id'

  return short_form_dictionary

def compare_columns(column1, column2, short_form_dictionary):
  """
  Compares two columns and returns True if they are considered to be the same column, False otherwise.

  Args:
    column1: The first column to compare.
    column2: The second column to compare.
    short_form_dictionary: A dictionary of common short forms and their full names.

  Returns:
    True if the two columns are considered to be the same column, False otherwise.
  """

  # Preprocess the column names.
  column1_preprocessed = preprocess_column_name(column1)
  column2_preprocessed = preprocess_column_name(column2)

  # Check if the column names are the same or if they match a short form in the dictionary.
  if column1_preprocessed == column2_preprocessed:
    return True
  elif column1_preprocessed in short_form_dictionary and column2_preprocessed == short_form_dictionary[column1_preprocessed]:
    return True
  elif column2_preprocessed in short_form_dictionary and column1_preprocessed == short_form_dictionary[column2_preprocessed]:
    return True
  else:
    # Check if the column names are similar enough.
    if fuzzywuzzy.ratio(column1_preprocessed, column2_preprocessed) >= 90:
      return True
    else:
      return False

def compare_tables(table1, table2):
  """
  Compares two tables and generates a similarity score between them based on their metadata and semantic analysis of the column names.

  Args:
    table1: The first table to compare.
    table2: The second table to compare.

  Returns:
    A similarity score between the two tables.
  """

  # Compare table names.
  name_similarity = 1 if table1.name == table2.name else 0.5

  # Compare column names.
  column_names_similarity = 0
  for column1 in table1.columns:
    for column2 in table2.columns:
      if compare_columns(column1, column2, short_form_dictionary=create_short_form_dictionary()):
        column_names_similarity += 1

  # Calculate overall similarity score.
  similarity_score = (name_similarity + column_names_similarity) / 2

  return similarity_score

# Example usage.
table1 = pd.DataFrame({'name': ['John Doe', 'Jane
