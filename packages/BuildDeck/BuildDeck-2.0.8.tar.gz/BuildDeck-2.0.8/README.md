
# BuildDeck

**BuildDeck** is a powerful CLI tool designed for automating the build, test, deployment, and management of services in your projects. It provides easy-to-use commands for handling Maven builds, Docker Compose setups, and Postman test executions.

## Features

- Automate Maven build, test, clean, and verification tasks.
- Manage Docker Compose setups with easy-to-use commands.
- Run automated Postman tests for your services.
- Flexible command options for specifying environments and services.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Options](#options)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install BuildDeck from PyPI using:

```bash
pip install BuildDeck
```

Or install it locally for development:

```bash
git clone https://github.com/yourusername/BuildDeck.git
cd BuildDeck
pip install -e .
```

## Usage

Once installed, you can use the `builddeck` command to run various tasks. Here are some examples:

### Build Services in Development Environment

```bash
builddeck --env dev mvn-build
```

### Test Specific Services

```bash
builddeck --env staging --services service1,service2 mvn-test
```

### Deploy All Services

```bash
builddeck --env prod deploy
```

### Run Docker Compose Setup

```bash
builddeck up
```

## Commands

- `mvn-build` - Build all services using Maven.
- `mvn-test` - Test all services using Maven.
- `mvn-clean` - Clean all services using Maven.
- `mvn-verify` - Verify all services using Maven.
- `test` - Run Postman tests for all services.
- `build` - Build and deploy all services.
- `deploy` - Deploy all services, run Docker Compose, and execute tests.
- `compose` - Generate Docker Compose file.
- `up` - Start Docker Compose services.
- `down` - Stop and remove Docker Compose services.

## Options

### Global Options

- `--env` - Specify the environment (e.g., `dev`, `staging`, `prod`). Default is an empty string.
- `--services` - Comma-separated list of services to include (e.g., `service1,service2`). Default is all services.

### Command-specific Options

- `-s` or `--single` - Operate on a single service instead of all services.

## Contributing

Contributions are welcome! To get started:

1. Fork this repository.
2. Create a new feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push the branch: `git push origin feature-name`.
5. Submit a pull request.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
