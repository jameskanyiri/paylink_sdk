
# PayLink Python SDK

  

[![PyPI version](https://img.shields.io/pypi/v/paylink-sdk.svg)](https://pypi.org/project/paylink-sdk/)

[![Python Versions](https://img.shields.io/pypi/pyversions/paylink-sdk.svg)](https://pypi.org/project/paylink-sdk/)

[![License](https://img.shields.io/github/license/yourusername/paylink-sdk.svg)](https://github.com/yourusername/paylink-sdk/blob/main/LICENSE)

A Python SDK for seamlessly interacting with PayLink MCP server. PayLink is an open-source framework designed to streamline payment integration for developers building AI agents and financial applications across Africa.

## What is PayLink?

PayLink is an open-source framework that leverages the Model Context Protocol (MCP) to expose a unified interface for accessing diverse payment providers across Africa—such as M-Pesa and Airtel Money—enabling seamless financial workflows without repetitive integration work.

### Why PayLink?

Africa's financial ecosystem is fragmented. Developers often rebuild custom integrations for each payment provider, leading to redundancy and reduced scalability. **PayLink solves this** by:

* Providing **standardized MCP tools** for payments, invoicing, and reconciliation

* Empowering **AI agents** to handle payments intelligently

* Enabling **SMEs and micro-merchants** to access modern financial infrastructure

* Supporting **local-first** development with a global vision

  

## Installation

  

```bash

pip  install  paylink-sdk

```

  

## Features

  

- Asynchronous API for efficient communication with PayLink services

- Tool discovery and execution capabilities

  

## Quick Start

  

### Basic Usage

  

```python

import asyncio

from paylink_sdk import PayLinkClient

  

async  def  main():

# Initialize the client

client = PayLinkClient()

# List available tools

tools = await client.list_tools()

print(f"Available tools: {[tool.name for tool in tools]}")

# Initiate an M-Pesa STK Push

result = await client.call_tool("stk_push", {

"phone": "254712345678",

"amount": 1,

"account_reference": "Test Payment",

"transaction_desc": "Test"

})

print(f"STK Push result: {result}")

  

asyncio.run(main())

```

  



  

## Currently Supported Payment Providers

  

PayLink SDK currently supports the following payment providers:

  

### M-Pesa (Safaricom)

- STK Push API

- STK Push Status

- QR Code Generation

  

*More providers are being added regularly.*

  

## Available Tools

  

Each payment provider is exposed as a **tool** under the MCP server:

  

### M-Pesa Tools

  

| Tool | Description |

|------|-------------|

| `stk_push` | Initiates an STK Push request to a phone |

| `stk_push_status` | Checks the status of a previous STK push |

| `generate_qr_code` | Generates a payment QR code |

  

### Planned Providers and Features

  

*  **Additional Mobile Money**: Airtel Money, T-Kash, MTN Mobile Money

*  **Banking Integrations**: PesaLink, Open Banking APIs

*  **Cross-Border Payments**: Integration with regional and international remittance platforms

*  **AI-Powered Payment Bots**: Enable AI agents to manage collections, invoicing, and reconciliation

  

## Development

  

### Prerequisites

  

- Python 3.8+

- MCP client library

  


  

## Contributing

  

Contributions are welcome! Please feel free to submit a Pull Request.

  

1. Fork the repository

2. Create your feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add some amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request

  

We're particularly interested in contributions that:

- Add support for new payment providers

- Improve the MCP implementation

- Enhance documentation and examples

- Fix bugs and improve test coverage

  

## License

  

This project is licensed under the MIT License - see the LICENSE file for details.

  

## Acknowledgements

  

- Built on the MCP (Model Context Protocal) library

- Inspired by the OpenAI function calling API design

- Developed to simplify financial integration across Africa

  

---

  

## Changelog

  

### 0.5.0

- Initial public release

- Base client implementation

- OpenAI adapter support

- M-Pesa integration (STK Push, Status Check, QR Code Generation)