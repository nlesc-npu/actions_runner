import docker

class DockerAPIError(Exception):
    pass

class DockerAPI:
    def __init__(self, image, name, runner_label, runner_name):
        self.runner_label = runner_label
        self.runner_name = runner_name
        self.container = None

        self.client = docker.from_env()

        # ulimit increase is needed for XRT
        ulimits = [docker.types.Ulimit(name="memlock", soft=128000000, hard=128000000)]
        # Expose GPU (kfd, dri) and NPU (accel) devices on host
        devices = ["/dev/kfd:/dev/kfd", "/dev/dri:/dev/dri", "/dev/accel:/dev/accel"]

        self.config = {
            "image": image,
            "auto_remove": True,
            "detach": True,
            "devices": devices,
            "hostname": name,
            "name": name,
            "ulimits": ulimits
        }

    def start(self, url, registration_token):
        if self.container is not None:
            if self.container.status == "running":
                raise DockerAPIError("Container already running")
            else:
                self.container.remove()

        config = self.config.copy()
        config["command"] = f"-u {url} -t {registration_token} -l {self.runner_label} -n {self.runner_name}"
        self.container = self.client.containers.run(**config)

    def wait(self):
        if self.container is not None:
            self.container.wait()
        self.container = None

    def stop(self):
        if self.container is not None:
            self.container.stop()
        self.container = None

    def logs(self, stream=False):
        if self.container is not None:
            if stream:
                for line in self.container.logs(stream=True):
                    yield line
            else:
                return self.container.logs()
        else:
            return "No container running"
