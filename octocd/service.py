import docker
import base64


def create_port_mapping(ports):
    port_map = {}

    for host_port, cont_port in ports.items():
        port_map[host_port] = (cont_port, 'tcp', 'host')

    return port_map


def create_service(script, name, image, ports):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    b64_script = base64.b64encode(script.encode())

    container_spec = docker.types.ContainerSpec(
        image=image,
        args=['sh', '-c', 'echo ${OCTOCD_SCRIPT} | base64 -d | /bin/sh -e'],
        env={
            'OCTOCD_SCRIPT': 'ZWNobyAidGVzdCBwYXJhbWV0ZXIi'
        }
    )

    port_map = create_port_mapping(ports)

    task_tmpl = docker.types.TaskTemplate(container_spec)
    endpoint_tmpl = docker.types.EndpointSpec(ports=port_map)

    try:
        service_id = client.create_service(task_tmpl, name=name, endpoint_spec=endpoint_tmpl)
    except docker.errors.APIError as e:
        return 'Docker API had the following error: {}'.format(e)

    return service_id


def remove_service(id):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    client.remove_service(id)

