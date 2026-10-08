# MCP Job Application Tracker

A Model Context Protocol (MCP) server that lets Claude read and update a
personal job-application tracker through natural language. Built to learn MCP
end to end by building a working server, connecting it to Claude Desktop, and
using it in real conversations.

The project is small on purpose. The point was to understand the MCP
architecture directly: how a server exposes tools, how a client discovers and
calls them, and where the dividing line sits between the two.

## What it does

Once connected to Claude Desktop, you can manage your job search in plain
language:

- "What jobs am I tracking so far?"
- "Add the application I just submitted to Acme for a Senior AI Consultant role, remote."

Claude decides which tool to call, pulls the arguments from the request, runs
the tool, and reports back. The application data persists in a local JSON file.

## Architecture

The project separates cleanly into two layers, which was the main design idea:

**Storage layer (`storage.py`)** is plain Python with no MCP involved. It reads
and writes a local JSON file and exposes two functions, one to add an
application and one to list them. It can be tested entirely on its own.

**MCP server layer (`server.py`)** is a thin wrapper that exposes those two
functions as tools Claude can call. Each tool is a decorated function whose
docstring tells Claude when to use it and whose type hints define the input
schema. The server communicates over stdio, the standard transport for a local
server that the client launches as a subprocess.

This separation meant the data logic could be verified before the protocol was
added on top, and it keeps the MCP layer almost trivially small.

## How MCP fits

The project is a hands-on illustration of the client/server split. The server
built here exposes capabilities. The client, Claude Desktop, is the side that
decides when to use them. The developer builds and describes the tools; the
model drives them. That inversion, building something Claude calls rather than
calling Claude, is the core idea MCP is built around.

## Tech

- Python
- The MCP Python SDK (2.x)
- Claude Desktop as the MCP client
- A local JSON file for storage

## Running it

Install the dependency:
pip install “mcp[cli]”


Register the server with Claude Desktop by adding an entry to
`claude_desktop_config.json` pointing at your Python interpreter and
`server.py`, then restart Claude Desktop. The server launches automatically and
its tools appear in the client.

Note: `applications.json` holds personal application data and is created on
first run. It is excluded from version control. See `applications.example.json`
for the data shape.

## What I took away

The most useful outcome was understanding when to build a server versus consume
a client, and why MCP matters: it turns a one-off integration into a capability
any MCP-compatible client can reuse, rather than logic buried inside a single
application. The build also surfaced the realistic friction of a young
ecosystem, from a library rename to a working-directory path bug, which is
where most of the actual learning happened.