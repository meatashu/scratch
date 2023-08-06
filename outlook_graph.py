import win32com.client
import py2neo

def analyze_emails(outlook, neo4j):
  """Analyzes the user's emails and clusters people into different sets of interaction groups.

  Args:
    outlook: An instance of the Outlook.Application object.
    neo4j: A connection object to the Neo4j database.
  """

  # Get the inbox folder object.
  inbox = outlook.GetDefaultFolder(6)

  # Get all the messages in the inbox.
  messages = inbox.Items

  # Create a graph database for storing the interactions.
  graph = py2neo.Graph()

  # Iterate over all the messages and store the interactions in the graph database.
  for message in messages:
    # Get the sender and recipient of the message.
    sender = message.SenderName
    recipient = message.ToRecipients[0]

    # Create a node for the sender and the recipient.
    sender_node = graph.create(name=sender)
    recipient_node = graph.create(name=recipient)

    # Create an edge between the sender and the recipient.
    graph.create(sender_node, "sent", recipient_node, {"interactions": 1})

    # Add the subject of the message to the sender and recipient nodes.
    sender_node["subject"] = message.Subject
    recipient_node["subject"] = message.Subject

    # Add the date of the message to the sender and recipient nodes.
    sender_node["date"] = message.DateReceived
    recipient_node["date"] = message.DateReceived

  # Iterate over all the edges in the graph database.
  for edge in graph.edges(data=True):
    # Get the sender and recipient of the edge.
    sender = edge["source"]["name"]
    recipient = edge["target"]["name"]

    # Check if the sender is a junior or a senior.
    if sender.endswith("jr"):
      sender_is_junior = True
    else:
      sender_is_junior = False

    if recipient.endswith("jr"):
      recipient_is_junior = True
    else:
      recipient_is_junior = False

    # If the sender and recipient have different seniority levels, then increment the counter for the corresponding group.
    if sender_is_junior != recipient_is_junior:
      if sender_is_junior:
        group_name = "seniors"
      else:
        group_name = "juniors"

      graph.nodes[sender]["groups"].append(group_name)
      graph.nodes[recipient]["groups"].append(group_name)

  # Cluster the people into different sets of interaction groups.
  clusters = graph.community(algorithm="label_propagation")

  # Print the clusters.
  for cluster in clusters:
    print(cluster)

def scan_outlook_and_store_interactions(outlook, neo4j):
  """Scans the user's Outlook and stores their interactions in Neo4j.

  Args:
    outlook: An instance of the Outlook.Application object.
    neo4j: A connection object to the Neo4j database.
  """

  # Get the inbox folder object.
  inbox = outlook.GetDefaultFolder(6)

  # Get all the messages in the inbox.
  messages = inbox.Items

  # Create a graph database for storing the interactions.
  graph = py2neo.Graph()

  # Iterate over all the messages and store the interactions in the graph database.
  for message in messages:
    # Get the sender and recipient of the message.
    sender = message.SenderName
    recipient = message.ToRecipients[0]

    # Create a node for the sender and the recipient.
    sender_node = graph.create(name=sender)
    recipient_node = graph.create(name=recipient)

    # Create an edge between the sender and the recipient.
    graph.create(sender_node, "sent", recipient_node, {"interactions": 1})

    # Add the subject of the message to the sender and recipient nodes.
    sender_node["subject"] = message.Subject
    recipient_node["subject"] = message.Subject

    # Add the date of the message to the sender and recipient nodes.
    sender_node["date"] = message.DateReceived
    recipient_node["date"] = message.DateReceived

  # Iterate over all the edges in the graph database.
  for edge in graph.edges(data=True):
    # Increment the number of interactions for the edge.
    edge["interactions"] += 1

  # Print the number of interactions stored in the graph database.
  print("Number of interactions stored: ", graph.nodes.count())

if __name__ == "__main__":
  # Create an instance of the Outlook.Application object.
  outlook = win32com.client.Dispatch("Outlook.Application")

  # Connect to the Neo4j database.
  neo4j = py2neo.Graph("bolt://localhost:7687", user="neo4j", password="password")

  # Scan the user's Outlook and store their interactions in Neo4j.
  scan_outlook_and_store_interactions(outlook, neo4j)
