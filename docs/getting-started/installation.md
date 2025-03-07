# Installation

This guide will help you install `ezvent` and its dependencies on your system.

## Prerequisites

!!! info ""
    Before installing `ezvent`, make sure you have:

    - **Python 3.11 or higher**: `ezvent` uses modern Python features that require recent versions
    - **PostgreSQL with PGMQ extension**: `ezvent` relies on PostgreSQL with the PGMQ message queue extension
    - **pip**: For package installation (comes with Python)

## Setting Up PostgreSQL and PGMQ

### 1. PostgreSQL Installation

=== "Ubuntu/Debian"

    ```bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib
    ```

=== "macOS (using Homebrew)"

    ```bash
    brew install postgresql
    brew services start postgresql
    ```

=== "Windows"

    Download and install PostgreSQL from the [official website](https://www.postgresql.org/download/windows/).

### 2. Installing PGMQ Extension

PGMQ is a PostgreSQL extension that adds message queue functionality to PostgreSQL.

!!! example ""
    Using Docker (recommended for development)

    ```bash
    docker run -d \
      --name pgmq-postgres \
      -e POSTGRES_PASSWORD=postgres \
      -p 5432:5432 \
      quay.io/tembo/pgmq-pg:latest
    ```

!!! note ""
    For manual installation, follow the instructions from the [PGMQ GitHub repository](https://github.com/tembo-io/pgmq).

## Installing `ezvent`

### Using pip (recommended)

The easiest way to install `ezvent` is using pip:

```bash
pip install ezvent
```

### Installing from Source

For the latest version or to contribute to development:

```bash
git clone https://github.com/yourusername/ezvent.git
cd ezvent
pip install -e .
```

## Verifying Installation

You can verify that `ezvent` is installed correctly by running:

```python
import ezvent
print(ezvent.__version__)
```

## Default Configuration

!!! info ""
    By default, `ezvent` will try to connect to PostgreSQL at:

    ```
    Host: localhost
    Port: 5432
    User: postgres
    Password: postgres
    Database: postgres
    ```

    If your PostgreSQL setup is different, you'll need to configure `ezvent`. See the [Configuration](../user-guide/configuration.md) section for details.

## Next Steps

- [Quick Start Guide](quick-start.md): Learn the basics of using `ezvent`
- [Configuration Reference](../user-guide/configuration.md): Learn how to configure `ezvent`
