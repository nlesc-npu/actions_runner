#!/usr/bin/env python
from dotenv import dotenv_values
import logging
import time

from actions_runner.github_api import GithubAPI
from actions_runner.docker_api import DockerAPI

logger = logging.getLogger("actions_runner")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting")

    config = dotenv_values()
    runner_label = config["RUNNER_LABEL"]
    access_token = config["TOKEN"]
    repos = config["REPOS"].split(";")
    interval = config.get("INTERVAL", 30)

    docker_api = DockerAPI(image="rocm-xrt-gh", name="github_runner")

    tstart = time.time()
    while True:
        for repo in repos:
            owner, repo_name = repo.split('/')

            github_api = GithubAPI(owner, repo_name, access_token)

            runs = github_api.get_runs(status="queued")
            logger.info(f"{repo}: {runs['total_count']} queued actions")
            if runs["total_count"] == 0:
                continue

            for run_idx, run in enumerate(runs["workflow_runs"]):
                jobs = github_api.get_jobs(run)
                logger.info(f"Run {run_idx}: Found {jobs['total_count']} jobs")
                for job in jobs["jobs"]:
                    if runner_label in job["labels"]:
                        logger.info("Job for this machine found, launching docker container")
                        url = f"https://github.com/{owner}/{repo_name}"
                        registration_token = github_api.get_registration_token()["token"]
                        docker_api.start(url, registration_token)
                        docker_api.wait()
                        logger.info("Job finished")

        while time.time() - tstart < interval:
            time.sleep(1)
        tstart = time.time()
