# Roundcube SMTP PythonEmail Sender

A Python script for sending HTML emails with CC functionality using SMTP and managing sent items via IMAP.

## Features

- Sends HTML-formatted emails using templates
- Supports multiple recipients with individual CC lists
- Saves sent emails to the sender's Sent folder
- Rate limiting between sends to avoid server restrictions
- Environment-based configuration
- CSV-based recipient management

## Prerequisites

- Python 3.6+
- Access to an SMTP/IMAP email server
- Required Python packages:

```bash
pip install python-dotenv
```

## Project Structure

```
roundcube-email-sender/
├── app.py              # Main application script
├── index.html         # HTML email template
├── recipients.csv     # Recipient list configuration
├── .env              # Environment configuration
├── .gitignore        # Git ignore file
└── README.md         # This file

```

## Configuration

### 1. Environment Variables (.env)

Create a `.env` file in the project root:

```env
export EMAIL_USER="your.email@domain.com"
export EMAIL_PASSWORD="your_password"
export SMTP_SERVER="your.smtp.server"
export SMTP_PORT=465
export SENDER_NAME="Your Name"
```

### 2. Recipients List (recipients.csv)

Create a CSV file with the following format:

```csv
to_email,cc_emails
recipient1@example.com,cc1@example.com;cc2@example.com
recipient2@example.com,cc3@example.com;cc4@example.com
```

- `to_email`: Primary recipient
- `cc_emails`: Semicolon-separated list of CC recipients

### 3. Email Template (index.html)

- Place your HTML email template in `index.html`
- Use absolute URLs for images
- Include both plain text and HTML versions

## Usage

1. Set up your environment:

```bash
# Clone the repository
git clone [repository-url]
cd roundcube-email-sender

# Install dependencies
pip install -r requirements.txt

# Configure your .env file
cp .env.example .env

# Edit .env with your credentials
```

2. Prepare your recipients list:

```bash
# Edit recipients.csv with your recipient list
nano recipients.csv
```

3. Run the script:

```bash
python app.py
```

## Features Explained

### Email Sending

The script provides robust email sending capabilities with several key features:

- HTML-formatted emails using customizable templates
- Support for both HTML and plain text versions
- Multiple CC recipients per email
- Intelligent rate limiting between sends to prevent server throttling
- Comprehensive error handling and reporting

### Recipient Management

The CSV-based recipient system offers flexible management:

- Easy-to-maintain recipient configuration
- Support for multiple TO recipients
- Individual CC lists for each primary recipient
- Simple update process for recipient lists

### Error Handling

The script includes comprehensive error management:

- Detailed error reporting and logging
- Continued operation even if individual sends fail
- Debug mode for SMTP communication troubleshooting
- Automatic retry mechanism for temporary failures

## Common Issues and Solutions

### 1. Authentication Failed

If you encounter authentication issues:

- Verify your email credentials in the .env file
- Double-check SMTP server settings
- Ensure less secure app access is enabled (if required)
- Confirm no two-factor authentication conflicts
- For debugging Roundcube authentication errors, refer to the [Roundcube Authentication issue](https://github.com/roundcube/roundcubemail/issues/8676).

### 2. Email Not in Sent Folder

If sent emails aren't appearing in the Sent folder:

- Verify IMAP server settings
- Check folder names match your email server configuration
- Confirm proper permissions are set
- Ensure IMAP sync is enabled
- For saving sent emails to the Sent folder in Roundcube, see the [Roundcube Forum discussion](https://www.roundcubeforum.net/index.php?topic=30404.0).

### 3. Rate Limiting

To handle rate limiting issues:

- Adjust the sleep time between sends
- Monitor your server's sending limits
- Watch for specific SMTP error messages
- Implement exponential backoff if needed

## Security Notes

### Credential Management

- Never commit the .env file to version control
- Use environment variables for all sensitive data
- Consider implementing application-specific passwords
- Regularly rotate credentials

### Best Practices

- Keep all dependencies updated to latest stable versions
- Implement proper input validation
- Use secure SMTP/IMAP connections (SSL/TLS)
- Monitor for suspicious activity

## Contributing

We welcome contributions! Here's how to help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your PR:
- Includes appropriate tests
- Updates documentation as needed
- Follows the existing code style
- Includes a clear description of changes

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you need help or have questions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation thoroughly
- Contact the maintainers

---

*Last updated: January 2025*
