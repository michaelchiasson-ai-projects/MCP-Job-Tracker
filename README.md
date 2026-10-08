# MCP Job Application Tracker

A Model Context Protocol (MCP) server that lets Claude manage a personal
job-application tracker through natural language. Built to learn MCP end to end
by building a working server, connecting it to Claude Desktop, and using it in
real conversations.

The project is small on purpose. The point was to understand the MCP
architecture directly: how a server exposes tools and prompts, how a client
discovers and calls them, and where the dividing line sits between the two.

## What it does

Once connected to Claude Desktop, you can manage your job search in plain
language:

- "What jobs am I tracking so far?"
- "Add the application I just submitted to Acme for a Senior AI Consultant role, remote."
- "Mark the Acme application as interviewing."
- "Delete the duplicate entry for Acme."
- "Give me my weekly application review."

Claude decides which tool to call, pulls the arguments from the request, runs
the tool, and reports back. The application data persists in a local JSON file.

## Capabilities

The server exposes a full set of actions plus one packaged workflow, covering
two of the three things an MCP server can provide (tools and prompts):

**Tools** (actions Claude calls):
- `add_application` — record a new application
- `list_applications` — show everything tracked
- `update_status` — move an application to interviewing, offer, rejected, etc.
- `delete_application` — remove an entry by id

**Prompt** (a reusable workflow the user triggers by name):
- `Weekly application review` — surfaces action items, follows up on top
  prospects, and flags any application with no update in over a week

## Architecture

The project separates cleanly into two layers, which was the main design idea:

**Storage layer (`storage.py`)** is plain Python with no MCP involved. It reads
and writes a local JSON file and exposes the four data operations (add, list,
update status, delete), each testable on its own. Applications are stamped with
a `last_updated` date on creation and on any status change, which is what makes
the staleness check in the weekly review meaningful. Ids are assigned from the
highest existing id so deletions never cause a collision.

**MCP server layer (`server.py`)** is a thin wrapper that exposes those
functions as tools Claude can call, plus one prompt. Each tool is a decorated
function whose docstring tells Claude when to use it and whose type hints define
the input schema. The prompt is a decorated function that returns an instruction
template; the client surfaces it as a one-click command, and Claude carries it
out using the tools. The server communicates over stdio, the standard transport
for a local server that the client launches as a subprocess.

This separation meant the data logic could be verified before the protocol was
added on top, and it keeps the MCP layer almost trivially small.

## How MCP fits

The project is a hands-on illustration of the client/server split. The server
built here exposes capabilities. The client, Claude Desktop, is the side that
decides when to use them. The developer builds and describes the tools and
prompts; the model drives them. That inversion, building something Claude calls
rather than calling Claude, is the core idea MCP is built around.

An MCP server can expose three kinds of things: tools (actions the model
chooses to call), prompts (reusable templates the user triggers), and resources
(data exposed for context). This project uses tools and a prompt. Resources
were left out deliberately, since the data is small and the list tool already
surfaces it on demand.

## Tech

- Python
- The MCP Python SDK (2.x)
- Claude Desktop as the MCP client
- A local JSON file for storage

## Running it

Install the dependency:

    pip install "mcp[cli]"

Register the server with Claude Desktop by adding an entry to
`claude_desktop_config.json` pointing at your Python interpreter and
`server.py`, then restart Claude Desktop. The server launches automatically.
Its tools become available to Claude, and the weekly review prompt appears in
the client's prompt menu.

Note: `applications.json` holds personal application data and is created on
first run. It is excluded from version control. See `applications.example.json`
for the data shape.

## What I took away

The most useful outcome was understanding when to build a server versus consume
a client, and why MCP matters: it turns a one-off integration into a capability
any MCP-compatible client can reuse, rather than logic buried inside a single
application. Building out the full tool set and a prompt also made the three
server capabilities concrete, including where a prompt fits (instructions the
model acts on) versus a tool (an action it takes). The build surfaced the
realistic friction of a young ecosystem too, from a library rename to a
working-directory path bug, which is where most of the actual learning happened.