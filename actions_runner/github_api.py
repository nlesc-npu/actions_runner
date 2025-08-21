import requests

class GithubAPIError(Exception):
    pass


class GithubAPI:
    def __init__(self, owner, repo, token=None):
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"

        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-Github-Api-Version": "2022-11-28"
        }

        if token is not None:
            self.headers["Authorization"] = f"Bearer {token}"

    @staticmethod
    def __check_api_call(request, expected_status_code):
        if request.status_code == 404:
            raise GithubAPIError("Page not found")
        elif request.status_code == 403:
            raise GithubAPIError("Permission denied, use a token if you are trying to access a private repo")
        elif request.status_code != expected_status_code:
            raise GithubAPIError(f"Expected status code to be {expected_status_code}, got {request.status_code}")

    def get_runs(self, status=None):
        params = {}
        if status is not None:
            params["status"] = status

        url = f"{self.base_url}/actions/runs"
        result = requests.get(url, headers=self.headers, params=params)
        self.__check_api_call(result, 200)
        return result.json()

    def get_jobs(self, run):
        url = run["jobs_url"]
        result = requests.get(url, headers=self.headers)
        self.__check_api_call(result, 200)
        return result.json()

    def get_registration_token(self):
        if "Authorization" not in self.headers:
            raise GithubAPIError("access token must be set")

        url = f"{self.base_url}/actions/runners/registration-token"
        result = requests.post(url, headers=self.headers)
        self.__check_api_call(result, 201)
        return result.json()
