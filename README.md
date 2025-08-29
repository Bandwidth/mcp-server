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

Environment variables are used to configure the Bandwidth MCP Server.
The server will respect both system environment variables and those configured via your AI agent.

The following variables will be required to use the server:

```sh
BW_USERNAME     # Your Bandwidth API User Username
BW_PASSWORD     # Your Bandwidth API User Password
```

The following variables are optional or conditionally required:

```sh
BW_ACCOUNT_ID               # Your Bandwidth Account ID. Required for most API operations.
BW_NUMBER                   # A valid phone number on your Bandwidth account. Used with our Messaging and MFA APIs. Must be in E164 format.
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

For a more comprehensive list of common use cases when which tools are required for each, check out our
[Common Use Cases Guide](common_use_cases.md).

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

### Goose CLI

1. Install [Goose CLI](https://block.github.io/goose/docs/getting-started/installation/)
    - We recommend configuring Goose to use `Allow Mode`. This will require user approval before Goose calls tools, which could prevent Goose from accidentally taking unwanted actions.
2. Add the Bandwidth MCP Server as a Command-line Extension

```shell
goose configure
```

Then follow the prompts like the example below.

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

> **_NOTE:_** If you configure environment variables with Goose, it will prioritize those over your system environment variables.

### Cursor

1. Install [Cursor](https://cursor.com/downloads)
2. Update your `.cursor/mcp.json` file to include the following object

```json
{
    "mcpServers": {
        "bw-mcp-server": {
            "command":"uvx",
            "args": ["--from", "/path/to/bandwidth-mcp-server", "start"],
            "env": {
                "BW_USERNAME": "<insert-bw-username>",
                "BW_PASSWORD": "<insert-bw-password>",
                "BW_MCP_TOOLS": "tools,to,enable",
                "BW_MCP_EXCLUDE_TOOLS": "tools,to,exclude",
            }
        }
    }
}
```

### VSCode (Copilot)

1. Within VSCode, open the Command Palette and search for `MCP: Add Server`.
2. Choose `Command (stdio)`, then enter the full command to start the server. (Example Below)

```shell
uvx --from /path/to/bandwidth-mcp-server start
```

3. Choose a name for the server (ie. `bw-mcp-server`) and select if you'd like it to be enabled Globally or only in the current workspace.
4. You can configure environment variables by opening the `mcp.json` file VSCode provides like the example below.

```json
{
    "servers": {
        "bw-mcp-server": {
            "type": "stdio",
            "command": "uvx",
            "args": ["--from", "/path/to/bandwidth-mcp-server", "start"],
            "env": {
                "BW_USERNAME": "<insert-bw-username>",
                "BW_PASSWORD": "<insert-bw-password>",
                "BW_MCP_TOOLS": "tools,to,enable",
                "BW_MCP_EXCLUDE_TOOLS": "tools,to,exclude",
            }
        }
    },
    "inputs": []
}
```

> **_NOTE:_** You may need to make sure MCP servers are enabled in VSCode to begin using the server. See the [official guide](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) for more info.

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
                "BW_MCP_TOOLS": "tools,to,enable",
                "BW_MCP_EXCLUDE_TOOLS": "tools,to,exclude",
            }
        }
    }
}
```

> **_NOTE:_** You can also run the server directly from our github repo by replacing
`/path/to/bandwidth-mcp-server` with: `git+https://github.com/Bandwidth/bandwidth-mcp-server.git`

> **_NOTE:_** We've noticed some issues with Claude not being able to see MCP resources. This could require you to manually enter some tool parameters normally included in our config resource.

### Running the Server Standalone

The MCP server can be run locally using either native python or uv.
When running this way, all environment variables MUST be set in your system environment.

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
- `generateMessagingCode` - Send MFA code via SMS
- `generateVoiceCode` - Send MFA code via voice call
- `verifyCode` - Verify a previously sent MFA code

## **Phone Number Lookup**
- `createLookup` - Create a phone number lookup request
- `getLookupStatus` - Get status of an existing lookup request

## **Voice & Call Management**
- `listCalls` - Returns a list of call events with filtering options
- `listCall` - Returns details for a single call event

## **Reporting & Analytics**
- `getReports` - Get history of created reports
- `createReport` - Create a new report instance
- `getReportStatus` - Get status of a report
- `getReportFile` - Download report file
- `getReportDefinitions` - Get available report definitions

## **Media Management**
- `listMedia` - List your media files
- `getMedia` - Download a specific media file
- `uploadMedia` - Upload a media file
- `deleteMedia` - Delete a media file

## **Messaging**
- `listMessages` - List messages with filtering options
- `createMessage` - Send SMS/MMS messages
- `createMultiChannelMessage` - Send multi-channel messages (RBM, SMS, MMS)

## **Address Management**
- `getAddressFields` - Get supported address fields by country
- `validateAddress` - Validate an address and get excluded features
- `listAddresses` - List all addresses
- `createAddress` - Create an address
- `getAddress` - Get an address by ID
- `updateAddress` - Update an address
- `listCityInfo` - List city info search results

## **Compliance**
- `listDocumentTypes` - List all accepted document types and metadata requirements
- `listEndUserTypes` - List all End user types and accepted metadata
- `listEndUserActivationRequirements` - List requirements for End user activation
- `getComplianceDocumentMetadata` - Get metadata of uploaded documents
- `updateComplianceDocument` - Modify document data and file
- `downloadComplianceDocuments` - Download document using document ID
- `createComplianceDocument` - Upload a document with metadata
- `listComplianceEndUsers` - List all End users of an account
- `createComplianceEndUser` - Create an End user
- `getComplianceEndUser` - Retrieve an End User by ID
- `updateComplianceEndUser` - Update End user details

## **Requirements Packages**
- `listRequirementsPackages` - List all requirements packages
- `createRequirementsPackage` - Create a requirements package
- `getRequirementsPackage` - Retrieve a requirements package
- `patchRequirementsPackage` - Update Requirements package
- `getRequirementsPackageAssets` - Get assets attached to requirements package
- `attachRequirementsPackageAsset` - Attach an asset to requirements package
- `detachRequirementsPackageAsset` - Detach an asset from requirements package
- `validateNumberActivation` - Validate number activation requirements
- `getRequirementsPackageHistory` - Get history of a requirements package
