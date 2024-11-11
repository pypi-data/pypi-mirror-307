import os
from builddeck.helpers.get_logging import logger

version_file = "versions.txt"

import requests
import re


def get_docker_image_version_tag(service_name):
    # Define the API URL for fetching the tags
    url = f"https://hub.docker.com/v2/repositories/leultewolde/{service_name}/tags/"

    # Send the GET request to the Docker Hub API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Extract the tag names
        tags = [result['name'] for result in data['results']]

        # Use a regex to match tags that start with a version number
        for tag in tags:
            match = re.match(r"^(\d+\.\d+\.\d+)", tag)  # Match tags like "1.0.30" at the start
            if match:
                return match.group(1)  # Return only the numeric version part
    else:
        print(f"Failed to fetch tags for {service_name}. Status code: {response.status_code}")
        return None


def increment_image_version(version):
    # Split the version into parts (e.g., "1.0.30" -> [1, 0, 30])
    version_parts = version.split('.')

    # Convert the parts to integers
    version_parts = [int(part) for part in version_parts]

    # Increment the last part of the version number
    version_parts[-1] += 1

    # Join the parts back into a string (e.g., [1, 0, 31] -> "1.0.31")
    incremented_version = '.'.join(map(str, version_parts))

    return incremented_version

# version_tag = get_docker_image_version_tag("user-service")
# print("Number Version Tag:", version_tag)
#
# if version_tag:
#     print("Current Version Tag:", version_tag)
#     incremented_version_tag = increment_image_version(version_tag)
#     print("Incremented Version Tag:", incremented_version_tag)

def initialize_version_file():
    """Create the version file if it doesn't exist."""
    if not os.path.exists(version_file):
        with open(version_file, "w") as f:
            f.write("Service Versions\n")
        logger.info("📁 Version file created", extra={"event": "file_created", "version_file": version_file})

def increment_version(version):
    """Increment the patch version of a semantic version string."""
    parts = version.split(".")
    if len(parts) == 3:
        parts[2] = str(int(parts[2]) + 1)  # Increment the patch version
    else:
        parts = ["1", "0", "0"]  # Default version if not found
    return ".".join(parts)


def save_version_to_file(version_data):
    """Save all service versions to the version file."""
    try:
        if not version_data:
            logger.error("Version data is empty, nothing to save", extra={"event": "save_version_failed"})
            return

        # Open the file in write mode (overwrite existing file)
        with open(version_file, "w") as f:
            logger.info("Saving versions to file", extra={"event": "save_version", "version_file": version_file})
            for service_name, version in version_data.items():
                f.write(f"{service_name}:{version}\n")
            f.flush()
            os.fsync(f.fileno())  # Force write to disk

        logger.info("✅ Version data successfully written to file", extra={"event": "save_version_success"})

    except OSError as e:
        logger.error(f"❌ Error opening/writing to file: {e}",
                     extra={"event": "save_version_failed", "version_file": version_file})


def read_version_data():
    """Read the current versions from the file."""
    version_data = {}
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if ":" in line:
                    service, version = line.strip().split(":")
                    version_data[service] = version
    return version_data

