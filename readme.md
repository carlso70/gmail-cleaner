# Gmail Cleanup Script

Don't pay for google one

This Python script automates the process of deleting emails older than one year from your Gmail account.

## Prereqs

- Google Cloud Console project with Gmail API enabled
- OAuth 2.0 credentials for a desktop application

## Setup

1. Clone this repository or download the script.

2. Install required libraries:

   ```
   pip install google-auth-oauthlib google-api-python-client
   ```

3. Set up Google Cloud Console project:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API for your project
   - Create OAuth 2.0 credentials (OAuth client ID, Desktop app)
   - Download the client configuration and save it as `credentials.json` in the same directory as the script

## Usage

1. Ensure `credentials.json` is in the same directory as the script.

2. Run the script:

   ```
   python delete_old_emails.py
   ```

3. On first run, the script will open a browser window. Log in to your Google account and grant the requested permissions.

4. The script will start processing emails, providing updates on its progress.

5. Upon completion, the script will display the total number of emails deleted and any errors encountered.

## Warning

This script will move ALL emails older than one year to the trash. Make sure this is what you want before running the script, as it could delete important emails. Consider backing up your emails before running this script.

## License

This project is open source and available under the [MIT License](LICENSE).
