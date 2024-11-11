import yaml

from builddeck.helpers.get_logging import logger
from builddeck.helpers.processes import run_command

class InlineListDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(InlineListDumper, self).increase_indent(flow=True, indentless=indentless)

    def represent_list(self, data):
        return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

# Register the custom Dumper behavior for lists
InlineListDumper.add_representer(list, InlineListDumper.represent_list)

# Function to generate dynamic Docker Compose
def generate_docker_compose(services, environment, additional_services=None, volumes = None):
    """Generate a Docker Compose file dynamically for the services based on environment."""
    if additional_services is None:
        additional_services = {}

    if volumes is None:
        volumes = {}

    compose = {
        'services': {},
        'networks': {
            'mereb_app-network': {
                'driver': 'bridge'
            }
        },
        'volumes': volumes
    }

    for service in services:
        # Dynamic ports and environment variables
        service_ports = service.get('ports', [])
        service_environment = service.get('environment', [])

        tag = f"{service['version']}-{environment}" if environment != 'production' else service['version']
        if service["version"] == 'latest' and environment != 'production':
            tag = f"{environment}-latest"

        env_file = {'env_file': service['env_file']} if service.get('env_file') else {}

        healthcheck = service.get('healthcheck', {})
        formatted_healthcheck = {
            "test": healthcheck.get("test", []),
            "interval": healthcheck.get("interval", "30s"),
            "timeout": healthcheck.get("timeout", "10s"),
            "retries": healthcheck.get("retries", 3),
            "start_period": healthcheck.get("start_period", "10s")
        } if healthcheck else None

        if formatted_healthcheck and isinstance(formatted_healthcheck.get("test"), list):
            formatted_healthcheck["test"] = [str(cmd) for cmd in formatted_healthcheck["test"]]

        container_name = service['name'] if environment == 'production' else f'{service["name"]}-{environment}'

        service_definition = {
            'image': f'leultewolde/{service["name"]}:{tag}',
            'container_name': container_name,
            'ports': service_ports,
            'environment': service_environment,
            'networks': ['mereb_app-network']
        }

        if env_file:
            service_definition.update(env_file)

        if formatted_healthcheck:
            service_definition['healthcheck'] = formatted_healthcheck

        compose['services'][service['name']] = service_definition

    compose['services'] = {
        **additional_services,
        **compose['services']
    }

    compose_file = 'docker-compose.yml' if environment in ['production', 'default'] else f'docker-compose.{environment}.yml'

    with open(compose_file, 'w') as file:
        yaml.dump(compose, file, default_flow_style=False, sort_keys=False, Dumper=InlineListDumper)

    logger.info(f"📝 Docker Compose file for {environment} environment generated as {compose_file}")
    return compose_file

def run_docker_compose(services, environment, is_build, additional_services, volumes):
    # Get the dynamic Docker Compose file
    compose_file = generate_docker_compose(services, environment, additional_services, volumes)

    build_command = f"docker-compose -f {compose_file} up -d"
    if is_build:
        build_command = build_command + " --build"
    # Bring up Docker containers
    logger.info("🚢 Bringing up Docker containers", extra={"event": "docker_compose_up"})
    run_command(build_command, event="docker_compose_up")
    logger.info("✅ All services have been built, tagged, pushed, and composed.", extra={"event": "deployment_complete"})
    logger.info(" 🎉 Deployment complete!")


def destroy_docker_compose(environment):
    logger.info("🛠️ Bringing down Docker containers", extra={"event": "docker_compose_down"})
    compose_file = f'docker-compose.yml' if environment == 'production' and environment == 'default' else f'docker-compose.{environment}.yml'
    run_command(f"docker-compose -f {compose_file} down", event="docker_compose_down")
