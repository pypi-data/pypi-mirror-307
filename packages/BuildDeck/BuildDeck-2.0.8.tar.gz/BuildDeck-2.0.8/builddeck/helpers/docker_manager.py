import docker
from docker.errors import ImageNotFound
from builddeck.helpers.get_logging import logger

class DockerManager:
    def __init__(self):
        # Initialize the Docker client
        self.client = docker.from_env()

    def get_container_by_name(self, service_name):
        """Retrieve the container object by name."""
        containers = self.client.containers.list()
        for container in containers:
            if service_name in container.name:
                return container
        return None

    def is_service_running(self, service_name):
        """Check if a service (container) is running by name."""
        container = self.get_container_by_name(service_name)
        return container and container.status == "running"

    def is_any_service_running(self, services):
        """Check if at least one service is running."""
        if any(self.is_service_running(service) for service in services):
            return True
        return False

    def is_service_running_and_healthy(self, service_name):
        """Check if a service is running and passes the health check."""
        container = self.get_container_by_name(service_name)
        if container and container.status == "running":
            health_status = container.attrs['State'].get('Health', {}).get('Status')
            if health_status == "healthy":
                logger.info(f"✅ {service_name} is running and healthy!", extra={"service_name": service_name})
                return True
            elif health_status:
                logger.warning(f"⚠️ {service_name} is running but not healthy (status: {health_status}).", extra={"service_name": service_name})
                return False
            else:
                logger.info(f"⚠️ {service_name} is running but no health check is defined.", extra={"service_name": service_name})
                return True
        logger.warning(f"❌ {service_name} is not running.", extra={"service_name": service_name})
        return False

    def image_exists(self, image_name):
        """Check if a Docker image exists."""
        try:
            self.client.images.get(image_name)
            return True
        except ImageNotFound:
            return False