import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_explorative_visualization(hive_table, hive_query):
  """Generates explorative visualization for the given Hive table and query.

  Args:
    hive_table: The name of the Hive table.
    hive_query: The Hive query to execute.

  Returns:
    A dictionary of explorative visualizations.
  """

  # Connect to Hive and execute the query.
  conn = hive.Connection('localhost', port=10000)
  cursor = conn.cursor()
  cursor.execute(hive_query)

  # Create a Pandas DataFrame from the Hive results.
  df = pd.DataFrame(cursor.fetchall())

  # Generate explorative visualizations for the DataFrame.
  visualizations = {}
  for column in df.columns:
    datatype = df[column].dtype

    if datatype == 'object':
      # For categorical data, generate a bar chart.
      visualizations[column] = df[column].value_counts().plot.bar()
    elif datatype == 'int64' or datatype == 'float64':
      # For numerical data, generate a histogram.
      visualizations[column] = df[column].plot.hist()
    else:
      # For other data types, generate a scatter plot.
      visualizations[column] = df[column].plot.scatter()

  return visualizations

def generate_profile_of_data(hive_table, hive_query):
  """Generates a profile of the given Hive table and query.

  Args:
    hive_table: The name of the Hive table.
    hive_query: The Hive query to execute.

  Returns:
    A dictionary of data profile.
  """

  # Connect to Hive and execute the query.
  conn = hive.Connection('localhost', port=10000)
  cursor = conn.cursor()
  cursor.execute(hive_query)

  # Create a Pandas DataFrame from the Hive results.
  df = pd.DataFrame(cursor.fetchall())

  # Generate a data profile of the DataFrame.
  profile = {}
  profile['number_of_rows'] = df.shape[0]
  profile['number_of_columns'] = df.shape[1]
  profile['column_datatypes'] = df.dtypes.to_dict()

  for column in df.columns:
    profile[column] = df[column].describe()

  return profile

if __name__ == '__main__':
  # Get the Hive table and query from the user.
  hive_table = input('Enter the name of the Hive table: ')
  hive_query = input('Enter the Hive query: ')

  # Generate explorative visualization for the Hive table and query.
  visualizations = generate_explorative_visualization(hive_table, hive_query)

  # Generate a profile of the data.
  profile = generate_profile_of_data(hive_table, hive_query)

  # Print the explorative visualizations.
  for column, visualization in visualizations.items():
    plt.show(visualization)

  # Print the data profile.
  print(profile)
