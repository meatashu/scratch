import hive
import difflib
import matplotlib.pyplot as plt

def compare_tables(table1, table2):
  """Compares two Hive tables and returns the similarity between their columns.

  Args:
    table1: The name of the first Hive table.
    table2: The name of the second Hive table.

  Returns:
    The similarity between the two tables, as a float between 0 and 1.
  """

  columns1 = hive.table(table1).columns
  columns2 = hive.table(table2).columns

  # Create a dictionary to store the similarity between each column pair.
  column_similarities = {}
  for column1 in columns1:
    for column2 in columns2:
      column_similarities[column1, column2] = difflib.SequenceMatcher(
          None, column1, column2).ratio()

  # Calculate the overall similarity between the two tables.
  total_similarity = 0
  for column1, column2 in column_similarities.keys():
    total_similarity += column_similarities[column1, column2]

  similarity = total_similarity / len(column_similarities)

  return similarity

def main():
  """The main function."""

  tables = ["table1", "table2", "table3", "table4"]

  # Calculate the similarity between each pair of tables.
  similarities = {}
  for table1 in tables:
    for table2 in tables:
      if table1 != table2:
        similarities[table1, table2] = compare_tables(table1, table2)

  # Plot the similarities as a graph.
  plt.plot([table1 for table1, _ in similarities.keys()],
           [similarity for _, similarity in similarities.values()])
  plt.xlabel("Table")
  plt.ylabel("Similarity")
  plt.show()

if __name__ == "__main__":
  main()
