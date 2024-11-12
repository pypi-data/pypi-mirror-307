# Forge Python SDK

[![PyPi version](https://img.shields.io/pypi/v/forgeapp-sdk?style=flat)](https://pypi.org/project/forgeapp-sdk) [![Documentation](https://img.shields.io/badge/documentation-informational)](https://docs.forgeapp.io/) [![Discord](https://img.shields.io/badge/discord-join-blueviolet)](https://forgeapp.io/discord)

[Forge](https://forgeapp.io) is a low code internal tooling platform built on top of [Forge](https://interval.com) that allows developer to build internal tools that integrate directly with their APIs. Forge provides a JavaScript SDK to allow developers to quickly develop Forge apps.

## Why choose Forge?

With Forge, **all of the code for generating your web UIs lives within your app's codebase.** Forge apps are just asynchronous functions that run in your service. Because these are just functions, you can access the complete power of your existing services. When you need to request input or display output, `await` any of our I/O methods to present a form to the user and your script will pause execution until input is received.

## Getting started

To get started with building your first Forge app, all you have to do is define an action. An Action represents a Forge app, which users can define inline or imported. Forge apps can run as a separate background process within your service or as a standalone service. You can get started and create a Forge app in just a few lines of code.

```python
from forgeapp_sdk import Forge, IO

# Initialize Forge
forge = Forge(api_key="<YOUR API KEY>", endpoint: 'wss://<YOUR FORGE SERVER WEBSOCKET URL>/websocket')

@forge.action
async def refund_customer_order(io: IO):
    name = await io.input.text("Order ID")
    return f"Successfully refunded order ID: {orderID}"


# Synchronously listen, blocking forever
forge.listen()
```

To not block, forge can also be run asynchronously using
`forge.listen_async()`. You must provide your own event loop.

The task will complete as soon as connection to Forge completes, so you
likely want to run forever or run alongside another permanent task.

```python
import asyncio, signal

loop = asyncio.get_event_loop()
task = loop.create_task(forge.listen_async())
def handle_done(task: asyncio.Task[None]):
    try:
        task.result()
    except:
        loop.stop()

task.add_done_callback(handle_done)
for sig in {signal.SIGINT, signal.SIGTERM}:
    loop.add_signal_handler(sig, loop.stop)
loop.run_forever()
```

Forge:

- Allows you create forge apps as code which integrates directly with your existing functions.
- Makes creating full-stack apps as easy as writing CLI scripts.
- Can scale from a handful of scripts to robust multi-user dashboards.

With Forge, you do not need to:

- Deploy and maintain additional endpoint and/or services to support your forge apps.
- Give Forge write access to your database or secrets (or give us _any_ of your credentials, for that matter).
- Work in an external IDE. Integrate directly with your developer environment.

## More about Forge

- 📖 [Documentation](https://docs.forgeapp.io/)
- 🌐 [Forge website](https://forgeapp.io)
- 💬 [Discord community](https://forgeapp.io/discord)

## Local Development

This project uses [Poetry](https://python-poetry.org/) for dependency
management

1. `poetry install` to install dependencies
2. `poetry shell` to activate the virtual environment

Tasks are configured using [poethepoet](https://github.com/nat-n/poethepoet)
(installed as a dev dependency).

- `poe demo [demo_name]` to run a demo (`basic` by default if `demo_name` omitted)
- `poe test` to run `pytest` (can also run `pytest` directly in virtual env)

Code is formatted using [Black](https://github.com/psf/black). Please configure
your editor to format on save using Black, or run `poe format` to format the
code before committing changes.

## Tests

_Note:_ Tests currently require a local instance of the Forge backend.

Tests use [pytest](https://docs.pytest.org/en/7.1.x/) and
[playwright](https://playwright.dev/python/).

Currently assumes the `test-runner@forgeapp.io` user exists already.
Run `yarn test` in the `web` directory at least once to create it before
running these.
