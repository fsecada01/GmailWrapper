# GmailWrapper

A Python module for interacting with the Gmail API.

## Features

*   Send emails
*   Read emails
*   Search emails
*   Delete emails
*   Mark emails as read/unread
*   Get email threads
*   Manage labels

## Installation

```bash
pip install gmailwrapper
```

## Usage

```python
from gmailwrapper import GmailWrapper

# Initialize the GmailWrapper
gmail = GmailWrapper(credentials_file='path/to/credentials.json', token_file='path/to/token.json')

# Send an email
gmail.send_message(to='recipient@example.com', subject='Test Email', body='This is a test email.')

# Search for emails
messages = gmail.search_messages(query='from:sender@example.com')

# Get a specific message
message = gmail.get_message(message_id='1234567890')

# Delete a message
gmail.delete_message(message_id='1234567890')

# Mark a message as read
gmail.mark_as_read(message_id='1234567890')

# Get all threads
threads = gmail.get_threads()

# Create a label
gmail.create_label(label_name='MyLabel')

# Add a label to a message
gmail.add_label_to_message(message_id='1234567890', label_name='MyLabel')

# Remove a label from a message
gmail.remove_label_from_message(message_id='1234567890', label_name='MyLabel')

# List all labels
labels = gmail.list_labels()
```

More information to be released in the near future.