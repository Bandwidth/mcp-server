# Bandwidth Official MCP Server
Source code for the official Bandwidth Model Context Protocol (MCP) Server.
This server can be used to interact with different Bandwidth APIs via an AI agent.
The server is provided as a python package and may be cloned directly from this repo.

## Installation

Clone directly from this git repository using:

```shell
git clone https://github.com/Bandwidth/bandwidth-mcp-server.git
cd bandwidth-mcp-server
```

## Getting Started

### Prerequisites

In order to use the Bandwidth MCP Server, you'll need the following things, set as environment variables.
- Valid Bandwidth API Credentials
    - This will be the username and password of your Bandwidth API user
    - For more info on creating API credentials, see our [Credentials](https://dev.bandwidth.com/docs/credentials) page
- Bandwidth Account ID
    - The ID of the account you'd like to make API calls on behalf of

### Configuration

#### Environment Variables

Environment variables can be set one of three ways for usage with the Bandwidth MCP Server:

1. System environment variables.
2. `.env` file - The package includes the `python-dotenv` package to allow reading from dotenv files.
3. Configured with your AI agent of choice - See our usage guides below.

The following variables will be required to use the server:

```sh
BW_ACCOUNT_ID   # Your Bandwidth Account ID
BW_USERNAME     # Your Bandwidth API User Username
BW_PASSWORD     # Your Bandwidth API User Password
```

The following variables are optional or conditionally required:

```sh
BW_NUMBER                   # A valid phone number on your Bandwidth account. Used with our Messaging and MFA APIs.
BW_MESSAGING_APPLICATION_ID # A Bandwidth Messaging Application ID. Used with our Messaging and MFA APIs.
BW_VOICE_APPLICATION_ID     # A Bandwidth Voice Application ID. Used with our MFA API.
BW_MCP_TOOLS                # The list of MCP tools you'd like to enable. If not set, all tools are enabled.
BW_MCP_EXCLUDE_TOOLS        # The list of MCP tools you'd like to exclude. Takes priority over BW_MCP_TOOLS.
```

#### Including or Excluding Tools

By default, the server provides and enables all tools listed in the [Tools List](#tools-list).
Enabling all of these tools may cause context window size issues for certain AI agents or lead to slower agent response times.
To work around this and for a better experience, we recommend enabling only the certain subset of tools you plan on using.

This can be accomplished by supplying a list of tool names to specifically enable or exclude to the server.
This list must be comma separated, with the tool names matching their names in the [Tools List](#tools-list).
The `BW_MCP_TOOLS` and `BW_MCP_EXCLUDE_TOOLS` mentioned in the [Environment Variables](#environment-variables)
section allow for enabling and excluding tools by name. You can also use the CLI flags `--tools` and `--exclude-tools`.
Using the CLI flags will take priority over the environment variables, and providing tools to exclude will take priority over the list of enabled tools.

##### Tool Filtering Examples

**Including only our Messaging tools**

```sh
# Environment Variable
BW_MCP_TOOLS=listMessages,createMessage,createMultiChannelMessage

# CLI Flag
--tools listMessages,createMessage,createMultiChannelMessage
```

**Excluding our Phone Number Lookup Tools**

```sh
# Environment Variable
BW_MCP_EXCLUDE_TOOLS=createLookup,getLookupStatus

# CLI Flag
--exclude-tools createLookup,getLookupStatus
```

## Using the Server

Below you'll find instructions for using our MCP server with different common AI agents, as well as instructions for running the server locally. For usage with AI agents, it is recommended to use a combination of [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#uv) and environment variables to start and configure the server respectively.

### Claude Desktop

1. Install [Claude Desktop](https://claude.ai/download)
2. Edit your `claude_desktop_config.json` to include the following object

```json
{
    "mcpServers": {
        "Bandwidth": {
            "command": "uvx",
            "args": ["--from", "/path/to/bandwidth-mcp-server", "start"],
            "env": {
                "BW_USERNAME": "<insert-bw-username>",
                "BW_PASSWORD": "<insert-bw-password>",
                "BW_ACCOUNT_ID": "<insert-bw-account-id>",
                "BW_MCP_TOOLS": "tools,to,enable",
                "BW_MCP_EXCLUDE_TOOLS": "tools,to,exclude",
            }
        }
    }
}
```

> **_NOTE:_**  You can also run the server directly from our github repo by replacing
`/path/to/bandwidth-mcp-server` with: `git+https://github.com/Bandwidth/bandwidth-mcp-server.git`

### Goose CLI

1. Install [Goose CLI](https://block.github.io/goose/docs/getting-started/installation/)
2. Add the Bandwidth MCP Server as an Extension

```shell
goose configure
```

Then follow the prompts like the example below, making sure to add all of the relevant environment variables at the end.

```shell
┌   goose-configure
│
◇  What would you like to configure?
│  Add Extension
│
◇  What type of extension would you like to add?
│  Command-line Extension
│
◇  What would you like to call this extension?
│  bw-mcp-server
│
◇  What command should be run?
│  uvx --from /path/to/bandwidth-mcp-server start
```

### Cursor

### Running the Server Standalone

The MCP server can be run locally using either native python or uv.

#### Run Using Native Python

Running the server locally with a python [virtual environment](https://docs.python.org/3/library/venv.html) requires both [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/getting-started/). 
Once these are installed, create a virtual environment using:

```sh
python -m venv .venv
```

Then activate and install the required packaged from the `requirements.txt` file.

```sh
source .venv/bin/activate
pip install -r requirements.txt
```

After all packages are installed in the virtual environment, you can run the server locally using:

```sh
python src/app.py
```

#### Run Using uv

Make sure you have [uv installed](https://github.com/astral-sh/uv?tab=readme-ov-file#installation),
then you can start the server by running the following command from the root directory of this repository.

```sh
uvx --from ./ start
```

## Tools List

## **Multi-Factor Authentication (MFA)**
- `bw-mcp-server__generateMessagingCode` - Send MFA code via SMS
- `bw-mcp-server__generateVoiceCode` - Send MFA code via voice call
- `bw-mcp-server__verifyCode` - Verify a previously sent MFA code

## **Phone Number Lookup**
- `bw-mcp-server__createLookup` - Create a phone number lookup request
- `bw-mcp-server__getLookupStatus` - Get status of an existing lookup request

## **Voice & Call Management**
- `bw-mcp-server__listCalls` - Returns a list of call events with filtering options
- `bw-mcp-server__listCall` - Returns details for a single call event

## **Reporting & Analytics**
- `bw-mcp-server__getReports` - Get history of created reports
- `bw-mcp-server__createReport` - Create a new report instance
- `bw-mcp-server__getReportStatus` - Get status of a report
- `bw-mcp-server__getReportFile` - Download report file
- `bw-mcp-server__getReportDefinitions` - Get available report definitions

## **Media Management**
- `bw-mcp-server__listMedia` - List your media files
- `bw-mcp-server__getMedia` - Download a specific media file
- `bw-mcp-server__uploadMedia` - Upload a media file
- `bw-mcp-server__deleteMedia` - Delete a media file

## **Messaging**
- `bw-mcp-server__listMessages` - List messages with filtering options
- `bw-mcp-server__createMessage` - Send SMS/MMS messages
- `bw-mcp-server__createMultiChannelMessage` - Send multi-channel messages (RBM, SMS, MMS)
