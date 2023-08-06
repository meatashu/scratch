import win32com.client

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

if __name__ == "__main__":
  # Create an instance of the Outlook.Application object.
  outlook = win32com.client.Dispatch("Outlook.Application")

  # Get the inbox folder object.
  inbox = outlook.GetDefaultFolder(6)

  # Categorize all emails in the inbox.
  categorize_emails(outlook, inbox)
