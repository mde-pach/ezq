# Installation

This guide will help you install EZQ and its dependencies on your system.

## Prerequisites

Before installing EZQ, make sure you have:

- **Python 3.11 or higher**: EZQ uses modern Python features that require recent versions
- **PostgreSQL with PGMQ extension**: EZQ relies on PostgreSQL with the PGMQ message queue extension
- **pip**: For package installation (comes with Python)

## Installing PostgreSQL and PGMQ

### 1. PostgreSQL Installation

#### On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### On macOS (using Homebrew):

```bash
brew install postgresql
brew services start postgresql
```

#### On Windows:

Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/windows/).

### 2. Installing PGMQ Extension

PGMQ is a PostgreSQL extension that adds message queue functionality to PostgreSQL.

#### Using Docker (recommended for development):

```bash
docker run -d \
  --name pgmq-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  quay.io/tembo/pgmq-pg:latest
```

#### Manual Installation:

Follow the installation instructions from the [PGMQ GitHub repository](https://github.com/tembo-io/pgmq).

## Installing EZQ

### Using pip (recommended)

The easiest way to install EZQ is using pip:

```bash
pip install ezq
```

### Installing from Source

For the latest version or to contribute to development:

```bash
git clone https://github.com/yourusername/ezq.git
cd ezq
pip install -e .
```

## Verifying Installation

You can verify that EZQ is installed correctly by running:

```python
import ezq
print(ezq.__version__)
```

## Configuration

By default, EZQ will try to connect to PostgreSQL at:

```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Database: postgres
```

If your PostgreSQL setup is different, you'll need to configure EZQ. See the [Configuration](../user-guide/configuration.md) section for details.

## Next Steps

- [Quick Start Guide](quick-start.md): Learn the basics of using EZQ
- [Configuration Reference](../user-guide/configuration.md): Learn how to configure EZQ
