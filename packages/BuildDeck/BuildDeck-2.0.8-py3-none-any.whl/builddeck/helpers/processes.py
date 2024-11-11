import os
import platform
import subprocess
import time
import sys

from builddeck.helpers.docker_manager import DockerManager
from builddeck.helpers.get_logging import logger
from builddeck.helpers.versioning import increment_image_version, get_docker_image_version_tag, increment_version, \
    save_version_to_file


def format_output(output, max_lines=10):
    """Limit the output to a reasonable number of lines."""
    lines = output.strip().split("\n")

    if len(lines) > max_lines:
        # Show the first 5 and last 5 lines with ellipsis in between
        limited_lines = lines[:10] + ["..."] + lines[-10:]
    else:
        limited_lines = lines

    return "\n".join(limited_lines)


# Minimal, interactive Maven/Docker logs
def run_command(command, ignore_errors=False, service_name=None, event=None):
    """Run a shell command and optionally ignore errors with interactive output logging."""
    logger.debug(f"🚀 Running command: {command}", extra={"event": event, "service_name": service_name})

    try:
        # Open the command using Popen for real-time streaming of stdout and stderr
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            # Stream stdout
            for stdout_line in iter(process.stdout.readline, ""):
                logger.info(stdout_line.strip(), extra={"event": event, "service_name": service_name})
            process.stdout.close()

            # Stream stderr
            for stderr_line in iter(process.stderr.readline, ""):
                logger.error(stderr_line.strip(), extra={"event": event, "service_name": service_name})
            process.stderr.close()

            # Wait for the process to complete and get the exit code
            return_code = process.wait()

            if return_code == 0:
                logger.info(f"✅ Command succeeded: {command}", extra={"event": event, "service_name": service_name})
            else:
                if ignore_errors:
                    logger.warning(f"⚠️ Command failed but continuing: {command}", extra={"event": event, "service_name": service_name})
                else:
                    logger.error(f"❌ Command failed: {command} (Exit Code: {return_code})", extra={"event": event, "service_name": service_name})
                    sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error occurred during command execution: {command} - {e}",
                     extra={"event": event, "service_name": service_name})
        if not ignore_errors:
            sys.exit(1)


def get_mvn_wrapper():
    system_name = platform.system()

    if system_name == "Windows":
        # On Windows, use 'mvnw.cmd'
        return "mvnw.cmd"
    else:
        # On Unix-like systems, use './mvnw'
        return "./mvnw"


def run_maven_command(command, service_name=None, event=None):
    wrapper = get_mvn_wrapper()
    if wrapper == "./mvnw":
        run_command(f"chmod +x {wrapper}", service_name=service_name, event=event)
    run_command(f"{wrapper} {command}", service_name=service_name, event=event)


def package_maven(service_name):
    logger.info(f"🛠️ Building {service_name} with Maven",
                extra={"event": "build_service", "service_name": service_name})
    run_maven_command("clean package", service_name=service_name, event="build_service")


def verify_maven(service_name):
    logger.info(f"🛠️ Verifying {service_name} with Maven",
                extra={"event": "verify_service", "service_name": service_name})
    run_maven_command("clean verify", service_name=service_name, event="verify_service")


def test_maven(service_name):
    logger.info(f"🛠️ Testing {service_name} with Maven",
                extra={"event": "test_service", "service_name": service_name})
    run_maven_command("clean test", service_name=service_name, event="build_service")


def clean_maven(service_name):
    run_maven_command("clean", service_name=service_name, event="clean_service")


def build_image_tag(version, environment):
    tag = f"{version}-{environment}"
    latest_tag = f"{environment}-latest"
    if environment == 'production':
        tag = version
        latest_tag = "latest"

    return tag, latest_tag


def package_and_build_docker_image(service_name, version, environment):
    package_maven(service_name)

    tag, latest_tag = build_image_tag(version, environment)
    image_name = f"leultewolde/{service_name}:{tag}"
    image_name_latest = f"leultewolde/{service_name}:{latest_tag}"

    dm = DockerManager()

    if dm.is_service_running(service_name):
        logger.info(f"🗑️ Stopping and removing Docker container for {service_name}",
                    extra={"event": "docker_cleanup", "service_name": service_name})
        run_command(f"docker stop {service_name}", ignore_errors=True, service_name=service_name,
                    event="stop_container")
        run_command(f"docker rm {service_name}", ignore_errors=True, service_name=service_name,
                    event="remove_container")
    if dm.image_exists(image_name):
        run_command(f"docker rmi {image_name}", ignore_errors=True, service_name=service_name, event="remove_image")
    if dm.image_exists(image_name_latest):
        run_command(f"docker rmi {image_name_latest}", ignore_errors=True, service_name=service_name, event="remove_image")

    logger.info(f"🛠️ Building Docker image for {service_name}",
                extra={"event": "docker_build", "service_name": service_name})
    run_command(f"docker build -t {image_name} .", service_name=service_name, event="build_docker_image")
    run_command(f"docker build -t {image_name} .", service_name=service_name, event="build_docker_image")

    return image_name, image_name_latest


def build_and_push_docker_images(service_name, version, environment):
    image_name, image_name_latest = package_and_build_docker_image(service_name, version, environment)

    logger.info(f"🚀 Pushing Docker image for {service_name}",extra={"event": "docker_build_push", "service_name": service_name})
    run_command(f"docker tag {image_name} {image_name_latest}", service_name=service_name, event="tag_docker_image")
    run_command(f"docker push {image_name}", service_name=service_name, event="push_docker_image")
    run_command(f"docker push {image_name_latest}", service_name=service_name, event="push_docker_image_latest")



def process_build_and_deploy(service_name, environment):
    new_version = increment_image_version(get_docker_image_version_tag(service_name))
    build_and_push_docker_images(service_name, new_version, environment)
    logger.info(f"✅ Service {service_name} processed successfully.",
                extra={"event": "process_service_success", "service_name": service_name})

def process_build_image(service_name, environment):
    """Build project with maven and create images"""
    new_version = increment_image_version(get_docker_image_version_tag(service_name))
    image_name, image_name_latest = package_and_build_docker_image(service_name, new_version, environment)
    logger.info(f"✅ Created images {image_name} and {image_name_latest} created successfully.",
                extra={"event": "process_service_success", "service_name": service_name})


def build_and_deploy_all_services(services, environment, working_dir=""):
    action = lambda service_name: process_build_and_deploy(service_name, environment)
    perform_action_on_all_services(services, action, working_dir)

def build_project_and_create_image_all_services(services, environment, working_dir=""):
    """Build project with maven and create images for all services"""
    action = lambda service_name: process_build_image(service_name, environment)
    perform_action_on_all_services(services, action, working_dir)

def package_all_services(services, working_dir=""):
    """RUN MVN PACKAGE ON ALL SERVICES"""
    action = lambda service_name: package_maven(service_name)
    perform_action_on_all_services(services, action, working_dir)


def maven_test_all_services(services, working_dir=""):
    """RUN MVN TEST ON ALL SERVICES"""
    action = lambda service_name: test_maven(service_name)
    perform_action_on_all_services(services, action, working_dir)


def clean_all_services(services, working_dir=""):
    """RUN MVN CLEAN ON ALL SERVICES"""
    action = lambda service_name: clean_maven(service_name)
    perform_action_on_all_services(services, action, working_dir)


def verify_all_services(services, working_dir=""):
    """RUN MVN VERIFY ON ALL SERVICES"""
    action = lambda service_name: verify_maven(service_name)
    perform_action_on_all_services(services, action, working_dir)


def perform_process_in_directory(process, path):
    try:
        os.chdir(path)
        process()
    except Exception as e:
        logger.error(f"❌ An error has occurred while processing in '{path}': {e}")
    finally:
        os.chdir("..")


def perform_action_on_all_services(services, action, working_dir=""):
    for service_name in services:
        path = working_dir + "/" + service_name
        logger.info(f"🚧 Processing {service_name}", extra={"event": "process_service", "service_name": service_name})
        process = lambda: action(service_name)
        perform_process_in_directory(process, path)


def process_service(service, version_data, environment):
    """Process building, tagging, and pushing Docker images for a service."""
    logger.info(f"🚧 Processing {service}", extra={"event": "process_service", "service_name": service})
    start_time = time.time()

    try:
        os.chdir(service)

        # Step 1: Build the service using Maven
        logger.info(f"🛠️ Building {service} with Maven", extra={"event": "build_service", "service_name": service})
        run_command("mvn clean package", service_name=service, event="build_service")

        # Step 2: Stop and remove the existing Docker container
        logger.info(f"🗑️ Stopping and removing Docker container for {service}",
                    extra={"event": "docker_cleanup", "service_name": service})
        run_command(f"docker stop {service}", ignore_errors=True, service_name=service, event="stop_container")
        run_command(f"docker rm {service}", ignore_errors=True, service_name=service, event="remove_container")

        # Step 3: Determine the current version and increment it
        version = version_data.get(service, "1.0.0")  # Default to 1.0.0 if not found
        new_version = increment_version(version)

        tag = f"{new_version}-{environment}"
        latest_tag = f"{environment}-latest"
        if environment == 'production':
            tag = new_version
            latest_tag = "latest"

        # Step 4: Build, tag, and push the Docker image with environment-specific tags
        logger.info(f"🚀 Building and pushing Docker image for {service}",
                    extra={"event": "docker_build_push", "service_name": service})
        run_command(f"docker build -t leultewolde/{service}:{tag} .", service_name=service, event="build_docker_image")
        run_command(f"docker tag leultewolde/{service}:{tag} leultewolde/{service}:{latest_tag}", service_name=service,
                    event="tag_docker_image")
        run_command(f"docker push leultewolde/{service}:{tag}", service_name=service, event="push_docker_image")
        run_command(f"docker push leultewolde/{service}:{latest_tag}", service_name=service,
                    event="push_docker_image_latest")

        # Step 5: Update the version in memory
        version_data[service] = new_version

        elapsed_time = time.time() - start_time
        logger.info(f"✅ Service {service} processed successfully in {elapsed_time:.2f} seconds.",
                    extra={"event": "process_service_success", "service_name": service})

    except Exception as e:
        logger.error(f"❌ An error occurred while processing {service}: {e}",
                     extra={"event": "process_service_failed", "service_name": service})
    finally:
        os.chdir("..")


def process_services(services, version_data, environment):
    for service in services:
        process_service(service["name"], version_data, environment)
        save_version_to_file(version_data)
