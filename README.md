# The Artificial Agent

Telegram bot that uses OpenAI's GPT-3 to generate responses to your messages with personality and personal assistant capabilities.

## Features

- Answers to your messages with [configurable](https://github.com/aitorllj93/the-artificial-agent/blob/main/config/config.example.yml) personality.
- Adds notes to your [Digital Brain (Obsidian)](#obsidian).

## Roadmap

- Integrate with ChatGPT API once it is released.
- Calendar meetings reminders.
- Mail notifications.
- Todo list.
- Digital Brain queries with gpt_index.

## Getting Started

### Prerequisites

- [Node.js v16.18](https://nodejs.org/en/download/)
- [Yarn](https://yarnpkg.com/getting-started)

### Installing

1. Clone the repo

   ```sh
   git clone https://github.com/aitorllj93/the-artificial-agent.git
   ```

2. Install NPM packages
   ```sh
   yarn install
   ```

### Configuration

1. Create a `config.yml` inside the config folder. You can use the `config.example.yml` as a template.

2. Add your Telegram bot token and (optionally) the Telegram chat id you will use. You can get your token [here](https://t.me/BotFather).

3. Add your OpenAI API key. You can get your key [here](https://platform.openai.com/account/api-keys).

### Usage

1. Run the bot

   ```sh
   yarn start
   ```

2. Send a message to your bot and wait for the response. (/start will be ignored)

### Integrations

#### [Obsidian](https://obsidian.md/)

##### Daily Notes

- Every time you ask the assistant to add a note, it will include it in your daily notes file. You can configure the path to your daily notes file in the config file.
