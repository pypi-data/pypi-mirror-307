# semarchy-xdi-runtime-client

## Installation

```bash
pip install semarchy-xdi-runtime-client
```

## What it does

This python package allow to remotly launch Semarchy XDI Delivery Job, by simply using the runtime url and the job name.
Variables can also be passed to the launch command.

## How it works

By using a network capture tool (Wireshark), an unofficial endpoints has been identified : `(runtime-url)/client/1`.  
This endpoint is used by the official start-command.sh command line tool when issuing a `launch delivery` command.

## How to use it

### As a CLI tool

While it's not the initial **objective** of this tool to replace the official CLI tool (start-command.sh), you can use it in script as a CLI.

The [documentation of the CLI]() details all available options.

### As a Python module
