import time

from builddeck.helpers.processes import run_command
from builddeck.helpers.get_logging import logger

from builddeck.helpers.docker_manager import DockerManager

def run_postman_tests(postman_key, postman_collection):
    """Run Postman tests if the services are running."""
    if postman_key and postman_collection:
        logger.info("🔧 Logging in to Postman", extra={"event": "postman_login"})
        run_command(f"postman login --with-api-key {postman_key}", event="postman_login")
        logger.info("🔧 Running Postman collection tests", extra={"event": "test_services"})
        run_command(f"postman collection run {postman_collection}", event="test_services")
        logger.info("🎉 Postman tests completed!")
    else:
        logger.error("❌ Postman test aborted due to missing API key or collection.")


class ServiceManager:
    def __init__(self, max_retries=10, retry_delay=10):
        self.dm = DockerManager()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def wait_for_service(self, service_name):
        """Wait for a service to be running and healthy with retries."""
        retries = 0
        while retries < self.max_retries:
            if self.dm.is_service_running_and_healthy(service_name):
                return True
            retries += 1
            self._log_retry(service_name, retries)
            time.sleep(self.retry_delay)
        logger.error(f"❌ {service_name} did not start after {self.max_retries} retries.", extra={"service_name": service_name})
        return False

    def wait_for_all_services(self, services):
        """Wait for all services to be running and healthy."""
        return all(self.wait_for_service(service) for service in services)

    def _log_retry(self, service_name, retries):
        logger.warning(f"🛠️ {service_name} retry {retries}/{self.max_retries}. Waiting {self.retry_delay} seconds...", extra={"service_name": service_name})

def test_all_services(services, postman_key, postman_collection):
    service_manager = ServiceManager()
    if service_manager.wait_for_all_services(services):
        if postman_key and postman_collection:
            run_postman_tests(postman_key, postman_collection)
    else:
        logger.error("❌ Postman test aborted due to API Gateway not running.")