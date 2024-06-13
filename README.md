# Project Title

This project is a Discord bot that uses the Mistral API to interact with users. It responds to user messages and handles events such as joining a new server or welcoming new members.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Discord.py library
- Mistral API access

### Installing

1. Clone the repository to your local machine.
2. Create a virtual environment named `venv`:

```bash
python -m venv venv
```

### Activate the virtual environment:
On Windows:
```
.\venv\Scripts\activate
```

On Unix or MacOS:
```
source venv/bin/activate
```

Install the required Python libraries using pip:
```
pip install -r requirements.txt
```

Create a .env file in the project root directory and add your Mistral API key and Discord client token:
```
MISTRAL_API_KEY = your_api_key_here
DISCORD_TOKEN = your_token
```

### Usage
Run the bot using the following command:

## Features
 - Chat Interaction: The bot responds to user messages using the Mistral API.
 - Server Joining: The bot prints a message when it joins a new server.
 - Member Welcoming: The bot triggers an event when a new member joins the server.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.