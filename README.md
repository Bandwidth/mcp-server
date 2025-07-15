# Bandwidth Official MCP Server
Source code for the official Bandwidth Model Context Protocol (MCP) Server. This server can be used to interact with different Bandwidth APIs via an AI agent. The server is provided as a PyPi package but may also be cloned directly from this repo.

## Installation

### Install from PyPi


### Install Locally

Clone directly from this git repository using:

```shell
git clone https://github.com/Bandwidth/bandwidth-mcp-server.git
cd bandwidth-mcp-server
```

## Prerequisites

In order to use the Bandwidth MCP Server, you'll need the following things, set as environment variables.
- Valid Bandwidth API Credentials
    - For more info on creating API credentials, see our [Credentials](https://dev.bandwidth.com/docs/credentials) page
- Bandwidth Account ID

Conditional Variables:
- Messaging Application ID
    - Necessary when using our Messaging API
- Bandwidth Telephone Number
    - 

## Getting Started

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
python app.py
```

#### Run Using uv

### Usage with Claude


### Usage with goose


### Configuration

### Environment Variables

#### Including or Excluding APIs

#### Including or Excluding Workflows

## List of all Tools Supplied by the Server

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
