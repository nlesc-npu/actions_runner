#!/usr/bin/env python
from dotenv import dotenv_values

from actions_runner.github_api import GithubAPI
from actions_runner.docker_api import DockerAPI


if __name__ == "__main__":
    # load token and repos from env
    config = dotenv_values()
    runner_label = config["RUNNER_LABEL"]
    access_token = config["TOKEN"]
    repos = config["REPOS"].split(";")

    docker_api = DockerAPI(image="rocm-xrt-gh", name="github_runner")

    # Check all repos once
    for repo in repos:
        print(f"Checking {repo}")
        owner, repo_name = repo.split('/')

        github_api = GithubAPI(owner, repo_name, access_token)

        # get all queued action runs
        runs = github_api.get_runs(status="queued")
        print(f"Found {runs['total_count']} queued actions")
        if runs["total_count"] == 0:
            continue

        for run_idx, run in enumerate(runs["workflow_runs"]):
            jobs = github_api.get_jobs(run)
            print(f"Run {run_idx}: Found {jobs['total_count']} jobs")
            for job in jobs["jobs"]:
                if runner_label in job["labels"]:
                    # job found that needs to be executed on this machine, spin up the container
                    print("Job for this machine found, launching container")
                    # Generate runner setup
                    url = f"https://github.com/{owner}/{repo_name}"
                    registration_token = github_api.get_registration_token()["token"]
                    docker_api.start(url, registration_token)
                    for line in docker_api.logs(stream=True):
                        print(line.decode().strip())
                    # wait for the job to finish
                    docker_api.wait()
                    print("Job finished")
