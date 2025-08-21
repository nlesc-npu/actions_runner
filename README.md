Automated self-hosted Github runner through Docker

Create a .env file in the root of the cloned repository with the following contents:
```
RUNNER_LABEL=<name of the runner as used in your workflow>
TOKEN=<your Github access token>
REPOS=owner1/repo1;owner2/repo2
INTERVAL=30  # optional, default set in main.py
```

Every `INTERVAL` seconds, the script will poll queued actions for all repos in `REPOS` one by one, and spin up a Docker container with Github Actions runner for each job that matches the runner label.
The Docker container is passed the repo url in the `URL` environment variable, and the runner registration token in `REG_TOKEN`. The container needs to take care of spinning up and registering an ephemeral Github Actions runner.

An example systemd service file is provided, edit this file as needed and copy it to `/etc/systemd/system/`. Reload with `systemctl daemon-reload`, enable the service with `systemctl enable actions_runner.service` and start it with `systemctl start actions_runner.service`. 


