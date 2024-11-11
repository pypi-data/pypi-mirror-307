# Gmail Automation Bot

A lightweight Python library for creating automated email response systems using Gmail. This bot monitors your Gmail inbox for new messages and responds to them automatically using a custom response function.

## Features

- 🔄 Continuous email monitoring
- ✨ Automatic responses to new emails
- 🚫 Built-in filtering for system emails
- 🔒 Secure authentication using Gmail App Passwords
- 📝 Customizable response function
- 🎯 Smart email threading with proper subject prefixing
- 💫 Beautiful terminal spinner animation during execution

## Installation

```bash
pip install imaplib email smtplib
```


## Quick Start

```python
from gmaillite import GmailAutomation

def response_func(subject, body):
    # Define your custom response logic here
    response = f"This is an automated response to your email: {body}"
    return response

# Initialize the bot with your credentials
gmail = GmailAutomation(response_func)

# Start the bot
gmail.start()
```

## Configuration Options

```python
GmailAutomation(
    response_func,                          # Your custom response function
    email_address='your.email@gmail.com',   # Gmail address
    app_password='your-app-password'        # Gmail App Password
)
```

### Starting the Bot

```python
# Start with default 2-second check interval
gmail.start()

# Or specify custom check interval (in seconds)
gmail.start(sleep_time=5)
```

## Custom Response Function

The response function receives two parameters:
- `subject`: The email subject
- `body`: The email body

Example:

```python
def response_func(subject, body):
    if "urgent" in subject.lower():
        return "I'll process your urgent request soon!"
    return f"Thank you for your email about: {subject}"
```

## Features in Detail

### Email Filtering
The bot automatically filters out system emails from:
- noreply addresses
- Google Community Team
- Google Play notifications
- Other automated system notifications

### Logging
Built-in logging system with:
- Info level logging for successful operations
- Error level logging for issues
- Debug level logging for system email filtering

### Error Handling
Robust error handling for:
- Email connection issues
- Authentication problems
- Message processing errors

## Security Notes

- Never commit your email credentials to version control
- Always use App Passwords instead of your main Gmail password
- Consider storing credentials in environment variables

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please open an issue on the GitHub repository.