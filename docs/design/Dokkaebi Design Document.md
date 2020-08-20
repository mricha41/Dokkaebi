# Dokkaebi

Dokkaebi is a Python library designed for the purposes of making Telegram Bot API use a snap. Dokkaebi provides two main mechanisms:

- A server to listen for updates from Telegram users
- A clean interface with which interactions with users can be managed

Dokkaebi server functionality depends upon the CherryPy library, while interactions are managed using the Requests library. Dokkaebi users only need to handle some basic configuration boilerplate along with inheriting from and decorating the Dokkaebi class. Overrides can be used to hook into processing at various stages in the pipeline, such as on construction, when updates are received from Telegram, as well as some other sensible stages.

## API

The Dokkaebi API wraps Telegram Bot API functionality, mirroring its use and replicating all of the functionality provided as completely as possible. See the [Telegram Bot API documentation](https://core.telegram.org/bots/api) for full details, including explanations regarding JSON data accepted and emitted by Telegram when using Dokkaebi to make requests. Because the Dokkaebi API is designed for programmers, this serves as its sole user interface.

## Functional Requirements

- Deploys to any server running Python 3.x
- Runs

## Non-Functional Requirements

- Easy to use
- Flexible
- Extensible
- Reasonably performant
- Simple deployment
- No build files
- Minimal dependencies

## Milestones

1. Implement all Telegram Bot API available method wrappers
2. Complete hooks for all stages in the bot pipeline
3. Complete serialization/deserialization helpers
4. Complete additional helpers as determined throughout development
5. Write tests
6. Configure continuous integration
7. Complete API Documentation
8. Complete Detailed Documentation (including examples/tutorials)
9. Release