import os
import re
import sys

import click
import yaml

from builddeck.helpers.config import load_config_new, ServiceNotFoundError
from builddeck.helpers.docker_compose import run_docker_compose, destroy_docker_compose, generate_docker_compose
from builddeck.helpers.get_logging import logger
from builddeck.helpers.processes import package_all_services, clean_all_services, verify_all_services, \
    build_and_deploy_all_services, maven_test_all_services, build_project_and_create_image_all_services


def get_current_version():
    try:
        setup_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'setup.py')
        print(setup_file)
        with open(setup_file, 'r') as file:
            setup_content = file.read()
            version_match = re.search(r"version=['\"]([^'\"]*)['\"]", setup_content)
            if version_match:
                return version_match.group(1)
            else:
                return "Unknown"
    except Exception:
        return "Unknown"


@click.group()
@click.option('--env', default='', help='Set the environment (e.g. dev, prod, staging)')
@click.option('--services', default='', help='Comma-separated list of services to include')
@click.pass_context
@click.version_option(version=get_current_version(), prog_name="BuildDeck", message="%(prog)s version %(version)s")
def cli(ctx, env, services):
    """BuildDeck CLI tool for automating services management tasks."""
    ctx.ensure_object(dict)
    ctx.obj['ENV'] = env
    ctx.obj['SERVICES'] = services.split(',') if services else []


def load_configuration(ctx):
    """Load configuration with context environment and services."""
    try:
        services, services_yml, environment, additional_services, volumes = load_config_new(ctx.obj['ENV'],
                                                                                            ctx.obj['SERVICES'])
        return services, services_yml, environment, additional_services, volumes
    except ServiceNotFoundError as e:
        logger.error(f"❌ Service not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


#
#   Initialize config files
#

@cli.command()
@click.pass_context
def init(ctx):
    """Create config file"""
    environment = "development" if ctx.obj['ENV'] == "dev" else "production" if ctx.obj[
                                                                                    'ENV'] == "prod" else "staging" if \
    ctx.obj['ENV'] == "staging" else "default"

    services = []
    for service in ctx.obj['SERVICES']:
        services.append({
            "name": service,
            "version": "latest",
            "ports": ["public:container"],
            "environment": [{"env1": "env1-value"}],
            "env_file": ".your.env",
            "healthcheck": [{"test": []}]
        })

    services_yml_file_contents = {
        'environment': environment,
        'services': services,
        'additional-services': {},
        'volumes': {}
    }

    file_name = f"services-{ctx.obj['ENV']}.yml" if ctx.obj['ENV'] else "services.yml"
    directory_path = 'build-deck'
    os.makedirs(directory_path, exist_ok=True)

    file_path = os.path.join(directory_path, file_name)

    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=True, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    try:
        with open(file_path, 'w') as file:
            yaml.dump(services_yml_file_contents, file, Dumper=MyDumper, default_flow_style=False, sort_keys=False,
                      indent=2)

        logger.info(f"📝 {file_name} created in `{file_path}`")
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


#
# MAVEN COMMANDS (test, build, clean, verify, install)
#

@cli.command()
@click.pass_context
def build(ctx):
    """Build all services using Maven Package"""
    try:
        services, _, _, _, _ = load_configuration(ctx)
        package_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def test(ctx):
    """Test all services using Maven test."""
    try:
        services, _, _, _, _ = load_configuration(ctx)
        maven_test_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def clean(ctx):
    """Clean all services using Maven clean."""
    try:
        services, _, _, _, _ = load_configuration(ctx)
        clean_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def verify(ctx):
    """Verify all services using Maven verify."""
    try:
        services, _, _, _, _ = load_configuration(ctx)
        verify_all_services(services, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


#
#   DOCKER COMMANDS (image, push, compose, down, up)
#

@cli.command()
@click.pass_context
def image(ctx):
    """Build and deploy all services."""
    try:
        services, _, environment, _, _ = load_configuration(ctx)
        build_project_and_create_image_all_services(services, environment, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def push(ctx):
    """Build and push all services."""
    try:
        services, _, environment, _, _ = load_configuration(ctx)
        build_and_deploy_all_services(services, environment, os.getcwd())
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def compose(ctx):
    """Generate Docker Compose file."""
    try:
        _, services_yml, environment, additional_services, volumes = load_configuration(ctx)
        generate_docker_compose(services_yml, environment, additional_services, volumes)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.option('-b', '--build', 'build_flag', is_flag=True, help='Operate on a single service instead of all services')
@click.pass_context
def up(ctx, build_flag):
    """Run Docker Compose."""
    try:
        _, services_yml, environment, additional_services, volumes = load_configuration(ctx)
        run_docker_compose(services_yml, environment, build_flag, additional_services, volumes)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def down(ctx):
    """Stop and remove Docker Compose services."""
    try:
        _, _, environment, _, _ = load_configuration(ctx)
        destroy_docker_compose(environment)
    except Exception as e:
        logger.error(f"❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    cli(obj={})
