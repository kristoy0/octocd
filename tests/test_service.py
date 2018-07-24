import docker
import pytest

from octocd import service


class TestService:
    def test_port_mapping(self):
        rv = service.create_port_mapping({8080: 80, 8443: 443})

        assert rv == {8080: (80, 'tcp', 'host'), 8443: (443, 'tcp', 'host')}

    def _service_creation(self):
        service_name = 'service-test'

        service_id = service.create_service('', service_name, 'nginx:latest',
                                            {8080: 80})

        return service_id, service_name

    def test_service_creation(self):
        client = docker.APIClient(base_url='unix://var/run/docker.sock')

        service_id, service_name = self._service_creation()

        rv_name = client.inspect_service(service_name)
        rv_id = client.inspect_service(service_id)

        assert rv_name
        assert rv_id

        service.remove_service(rv_id)

    def test_service_creation_fail(self):
        service_id, _ = self._service_creation()
        rv, _ = self._service_creation()

        assert 'Docker API had the following error:' in rv

        service.remove_service(service_id)

    def test_service_removal(self):
        client = docker.APIClient(base_url='unix://var/run/docker.sock')

        service_id, _ = self._service_creation()

        service.remove_service(service_id)

        with pytest.raises(docker.errors.NotFound):
            client.inspect_service(service_id)
