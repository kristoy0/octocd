import docker


def create_port_mapping(ports):
    port_map = {}

    for host_port, cont_port in ports.items():
        port_map[host_port] = (cont_port, 'tcp', 'host')

    return port_map


def create_service(script, name, image, ports):
    client = docker.APIClient(base_url='unix://var/run/docker.sock')

    container_spec = docker.types.ContainerSpec(
        image=image
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

