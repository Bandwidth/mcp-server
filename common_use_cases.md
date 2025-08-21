# Common Use Cases

This guide outlines some common use cases for the MCP Server, as well as the tools required for these cases.
For more information on how to include the tools mentioned in this guide, please see the
[Including or Excluding Tools](README.md#including-or-excluding-tools) section in the README.

## Sending Text Messages

If you're looking to send messages using the MCP server, we recommend enabling the following tools:
- `listMessages` - Get info about messages you just sent or other messages on your account.
- `createMessage` - Send SMS or MMS messages
- `createMultiChannelMessage` - Send multi-channel messages (mostly for RBM messaging)

**Enabling these tools**
```sh
# Environment Variable
BW_MCP_TOOLS=listMessages,createMessage,createMultiChannelMessage

# CLI Flag
--tools listMessages,createMessage,createMultiChannelMessage
```

## Looking up Telephone Numbers

If you'd like to get info about a specific telephone number or list of numbers,
you'll need both our `createLookup` and `getLookupStatus` tools.
Most agents we've experimented with have been smart enough to figure out that you
need to both create a lookup request and then get its' status to actually get the TN info,
and enabling only these two tools is a good way to help your agent remember that!

**Enabling these tools**
```sh
# Environment Variable
BW_MCP_TOOLS=createLookup,getLookupStatus

# CLI Flag
--tools createLookup,getLookupStatus
```

## Utilizing our MFA Service

To create and verify multi-factor authentication codes, you'll need our three MFA tools.
- `generateMessagingCode` - Used to generate and send an MFA code via SMS
- `generateVoiceCode` - Use to generate and send an MFA code via a phone call
- `verifyCode` - Verify an MFA code sent with one of the previous tools

**Enabling these tools**
```sh
# Environment Variable
BW_MCP_TOOLS=generateMessagingCode,generateVoiceCode,verifyCode

# CLI Flag
--tools generateMessagingCode,generateVoiceCode,verifyCode
```
