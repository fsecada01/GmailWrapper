# 📧 GmailWrapper

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> A modern, async-first Python library for seamless Gmail API integration with enterprise-grade architecture.

## ✨ Features

| Feature | Status | Description |
|---------|--------|-------------|
| 📤 **Send Emails** | ✅ | Send HTML/plain text emails with attachments |
| 📥 **Read Messages** | ✅ | Retrieve and parse email messages |
| 🔍 **Search & Filter** | ✅ | Advanced Gmail search with query parameters |
| 🗂️ **Thread Management** | ✅ | Handle email conversations and threads |
| 📝 **Draft Operations** | ✅ | Create, update, and manage email drafts |
| 🛡️ **Error Handling** | ✅ | Comprehensive exception hierarchy |
| ⚡ **Async Support** | ✅ | Full async/await support for high performance |
| 🏗️ **Modular Design** | ✅ | Clean separation of concerns |

## 🚀 Quick Start

### Installation

```bash
pip install gmailwrapper
```

### Basic Usage

```python
import asyncio
from gmailwrapper import GmailAPICaller

async def main():
    # Initialize the Gmail client
    gmail = GmailAPICaller()
    
    # Create and send an email
    message = gmail.create_message(
        sender="you@example.com",
        to="recipient@example.com", 
        subject="Hello from GmailWrapper! 🎉",
        message_text="This is a plain text message.",
        message_html="<h1>This is an HTML message!</h1><p>Pretty cool, right?</p>"
    )
    
    # Send the message
    result = await gmail.send_message(message)
    print(f"✅ Message sent! ID: {result['id']}")
    
    # Don't forget to close the client
    await gmail.close()

# Run the async function
asyncio.run(main())
```

## 📚 Comprehensive Examples

### 🔐 Authentication Setup

First, set up your Google Cloud credentials:

1. **Create a Google Cloud Project** at [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable the Gmail API** for your project
3. **Create OAuth2 credentials** and download the `credentials.json` file
4. **Set environment variables**:
   ```bash
   export BACKEND_DIR="/path/to/your/credentials"  # Optional, defaults to "./backend"
   export FLOW_PORT="8080"  # Optional, defaults to 5000
   ```

### 📤 Sending Different Types of Emails

```python
import asyncio
from gmailwrapper import GmailAPICaller

async def send_emails_example():
    gmail = GmailAPICaller()
    
    # 1. Simple text email
    simple_message = gmail.create_message(
        sender="your-email@gmail.com",
        to="recipient@example.com",
        subject="Simple Text Email",
        message_text="Hello! This is a simple text email."
    )
    await gmail.send_message(simple_message)
    print("✅ Simple email sent!")
    
    # 2. HTML email with CC
    html_message = gmail.create_message(
        sender="your-email@gmail.com",
        to="recipient@example.com",
        cc=["cc1@example.com", "cc2@example.com"],
        subject="Rich HTML Email 🎨",
        message_text="Fallback text for non-HTML clients.",
        message_html="""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #4CAF50;">Welcome to GmailWrapper!</h2>
                <p>This email was sent using our <strong>async Gmail API wrapper</strong>.</p>
                <ul>
                    <li>✅ Clean, modern architecture</li>
                    <li>⚡ Async/await support</li>
                    <li>🛡️ Robust error handling</li>
                </ul>
                <p><em>Happy coding!</em></p>
            </body>
        </html>
        """
    )
    await gmail.send_message(html_message)
    print("✅ HTML email with CC sent!")
    
    await gmail.close()

asyncio.run(send_emails_example())
```

### 📥 Reading and Managing Messages

```python
import asyncio
from gmailwrapper import GmailAPICaller, GmailAPIError

async def message_management_example():
    gmail = GmailAPICaller()
    
    try:
        # Get all messages (summary only)
        print("📬 Fetching message summaries...")
        messages = await gmail.get_messages()
        print(f"Found {len(messages)} messages")
        
        # Get detailed information for first 5 messages
        print("📖 Fetching detailed message info...")
        detailed_messages = await gmail.get_messages(details=True)
        
        for msg in detailed_messages[:5]:
            print(f"  📧 Subject: {msg.get('payload', {}).get('headers', [{}])[0].get('value', 'No subject')}")
            print(f"     ID: {msg['id']}")
            print(f"     Thread: {msg['threadId']}")
            print("  " + "─" * 50)
            
        # Get a specific message
        if messages:
            first_message_id = messages[0]['id']
            message = await gmail.get_message(first_message_id)
            print(f"📩 Retrieved message: {message['id']}")
            
            # Parse message content if needed
            if 'raw' in message:
                parsed = gmail.get_msg_from_str(message['raw'])
                print(f"   From: {parsed.get('From')}")
                print(f"   Subject: {parsed.get('Subject')}")
    
    except GmailAPIError as e:
        print(f"❌ Gmail API error: {e}")
        print(f"   Status code: {e.status_code}")
    
    await gmail.close()

asyncio.run(message_management_example())
```

### 🗂️ Working with Email Threads

```python
import asyncio
from gmailwrapper import GmailAPICaller

async def thread_management_example():
    gmail = GmailAPICaller()
    
    # Get all threads
    print("🧵 Fetching email threads...")
    threads = await gmail.get_threads()
    print(f"Found {len(threads)} threads")
    
    # Get detailed thread information
    if threads:
        thread_id = threads[0]['id']
        thread_detail = await gmail.get_thread(thread_id)
        
        print(f"📎 Thread {thread_id}:")
        print(f"   Messages in thread: {len(thread_detail.get('messages', []))}")
        
        # You can also delete entire threads
        # await gmail.delete_thread(thread_id)
        # print(f"🗑️  Thread {thread_id} moved to trash")
        
        # And restore them
        # await gmail.undelete_thread(thread_id)
        # print(f"♻️  Thread {thread_id} restored")
    
    await gmail.close()

asyncio.run(thread_management_example())
```

### 📝 Draft Management

```python
import asyncio
from gmailwrapper import GmailAPICaller

async def draft_management_example():
    gmail = GmailAPICaller()
    
    # Create a draft
    draft_message = gmail.create_message(
        sender="your-email@gmail.com",
        to="recipient@example.com",
        subject="Draft Email 📝",
        message_text="This is a draft message that I'll send later!"
    )
    
    # Save as draft
    draft = await gmail.create_draft(draft_message)
    print(f"✍️  Draft created with ID: {draft['id']}")
    
    # List all drafts
    drafts = await gmail.get_drafts()
    print(f"📄 Found {len(drafts)} drafts")
    
    # Get detailed draft information
    if drafts:
        draft_detail = await gmail.get_draft(drafts[0]['id'])
        print(f"📋 Draft details: {draft_detail['id']}")
        
        # Update the draft
        updated_message = gmail.create_message(
            sender="your-email@gmail.com",
            to="recipient@example.com",
            subject="Updated Draft Email ✏️",
            message_text="This draft has been updated with new content!"
        )
        
        updated_draft = await gmail.update_draft(drafts[0]['id'], updated_message)
        print(f"✏️  Draft updated: {updated_draft['id']}")
        
        # Clean up - delete the draft
        # await gmail.delete_draft(drafts[0]['id'])
        # print("🗑️  Draft deleted")
    
    await gmail.close()

asyncio.run(draft_management_example())
```

## 🏗️ Advanced Architecture

GmailWrapper is built with a clean, modular architecture:

```python
from gmailwrapper import (
    GmailAPICaller,      # Main interface (backwards compatible)
    GmailAuthenticator,  # Handles OAuth2 authentication  
    GmailHTTPClient,     # HTTP client with error handling
    GmailMessages,       # Message operations
    GmailDrafts,         # Draft operations  
    GmailThreads,        # Thread operations
    GmailConfig,         # Configuration management
    # Custom exceptions
    GmailWrapperError, GmailAuthError, GmailAPIError
)

# Use individual components for fine-grained control
async def advanced_usage():
    # Direct component usage
    config = GmailConfig()
    authenticator = GmailAuthenticator()
    client = GmailHTTPClient(authenticator, config.BASE_URL)
    
    # Work with specific resources
    messages = GmailMessages(client, config)
    all_messages = await messages.get_all(details=True)
    
    await client.close()
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_DIR` | `"./backend"` | Directory containing credentials and tokens |
| `FLOW_PORT` | `5000` | Port for OAuth2 callback server |
| `EMAIL_SIGNATURE` | `""` | Default email signature |
| `HTTP_PROXY` | `None` | HTTP proxy URL for requests |

### File Structure

```
your-project/
├── backend/                 # Credential storage (or custom BACKEND_DIR)
│   ├── credentials.json     # OAuth2 client credentials
│   └── token.json          # Generated access token (auto-created)
├── your_script.py
└── requirements.txt
```

## 🚨 Error Handling

GmailWrapper provides comprehensive error handling:

```python
import asyncio
from gmailwrapper import (
    GmailAPICaller,
    GmailAuthError,
    GmailCredentialsError,
    GmailAPIError,
    GmailRequestError
)

async def error_handling_example():
    try:
        gmail = GmailAPICaller()
        messages = await gmail.get_messages()
        await gmail.close()
        
    except GmailCredentialsError as e:
        print(f"❌ Credentials issue: {e}")
        print("💡 Make sure your credentials.json file exists and is valid")
        
    except GmailAuthError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 Check your OAuth2 setup and scopes")
        
    except GmailAPIError as e:
        print(f"❌ Gmail API error: {e}")
        print(f"   Status: {e.status_code}")
        print(f"   Response: {e.response}")
        
    except GmailRequestError as e:
        print(f"❌ Network error: {e}")
        print("💡 Check your internet connection")

asyncio.run(error_handling_example())
```

## 🔧 Development

### Requirements

- Python 3.10+
- httpx for async HTTP requests
- Google Auth libraries
- loguru for logging

### Code Quality

This project uses modern Python development tools:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code
black gmailwrapper/
isort gmailwrapper/

# Lint code  
ruff check gmailwrapper/

# Run pre-commit hooks
pre-commit run --all-files
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- 📚 [Documentation](https://github.com/fsecada01/GmailWrapper)
- 🐛 [Report Issues](https://github.com/fsecada01/GmailWrapper/issues)
- 💬 [Discussions](https://github.com/fsecada01/GmailWrapper/discussions)

---

<div align="center">
    <p>Made with ❤️ by <a href="https://github.com/fsecada01">Francis Secada</a></p>
    <p><em>Simplifying Gmail API integration, one async call at a time.</em></p>
</div>