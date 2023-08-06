import win32com.client
import nltk
import pandas as pd

def analyze_response(sender, response):
  """Analyzes the given response to the sender and determines the networking level.

  Args:
    sender: The name of the sender.
    response: The text of the response.

  Returns:
    The networking level between the user and the sender.
  """

  # Tokenize the response.
  tokens = nltk.word_tokenize(response)

  # Create a dictionary of entities.
  entities = {}
  for token in tokens:
    if nltk.pos_tag([token])[0][1] == "NNP":
      entities[token] = 1

  # Create a dictionary of keywords.
  keywords = {}
  for token in tokens:
    if len(token) > 3 and token not in entities:
      keywords[token] = 1

  # Determine the sentiment of the response.
  sentiment = nltk.sentiment.vader.SentimentIntensityAnalyzer().polarity_scores(response)

  # Create a Pandas DataFrame with the insights.
  insights = pd.DataFrame({
    "Entities": list(entities.keys()),
    "Keywords": list(keywords.keys()),
    "Sentiment": sentiment["compound"]
  })

  # Determine the networking level.
  if "meet" in keywords or "coffee" in keywords or "lunch" in keywords:
    networking_level = "Strong"
  elif "work" in keywords or "project" in keywords or "collaborate" in keywords:
    networking_level = "Medium"
  else:
    networking_level = "Weak"

  return networking_level

def analyze_email(email_body):
  """Analyzes the given email body using NLP and generates insights.

  Args:
    email_body: The text of the email body.

  Returns:
    A Pandas DataFrame containing the insights generated from the NLP analysis.
  """

  # Tokenize the email body.
  tokens = nltk.word_tokenize(email_body)

  # Create a dictionary of entities.
  entities = {}
  for token in tokens:
    if nltk.pos_tag([token])[0][1] == "NNP":
      entities[token] = 1

  # Create a dictionary of keywords.
  keywords = {}
  for token in tokens:
    if len(token) > 3 and token not in entities:
      keywords[token] = 1

  # Determine the sentiment of the email.
  sentiment = nltk.sentiment.vader.SentimentIntensityAnalyzer().polarity_scores(email_body)

  # Create a Pandas DataFrame with the insights.
  insights = pd.DataFrame({
    "Entities": list(entities.keys()),
    "Keywords": list(keywords.keys()),
    "Sentiment": sentiment["compound"]
  })

  return insights
def categorize_emails(outlook, inbox):
  """Categorizes all emails in the given inbox.

  Args:
    outlook: An instance of the Outlook.Application object.
    inbox: The Outlook folder object that represents the inbox.
  """

  messages = inbox.Items

  for message in messages:
    # Get the sender and subject of the email.
    sender = message.SenderName
    subject = message.Subject

    # Create a category for the email based on the sender and subject.
    category = "Personal"
    if sender == "John Smith":
      category = "Work"
    elif subject == "Invoice":
      category = "Finance"


    # Set the category for the email.
    message.Categories = category

    # Flag the thread if the user has replied to it more than once and where the user is not in the To field directly.
    if message.ReplyCount > 1 and sender not in message.ToRecipients:
      message.Flagged = True
    if "question" in message.Body and sender not in message.ToRecipients:
      message.Flagged = True


if __name__ == "__main__":
  # Create an instance of the Outlook.Application object.
  outlook = win32com.client.Dispatch("Outlook.Application")

  # Get the inbox folder object.
  inbox = outlook.GetDefaultFolder(6)

  # Categorize all emails in the inbox.
  categorize_emails(outlook, inbox)
