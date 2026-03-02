import requests

class GitHubStats:
    def __init__(self, username):
        self.username = username

    def query(self):
        url = f'https://api.github.com/users/{self.username}/repos'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def get_stats(self):
        repos = self.query()
        stats = {'public': 0, 'private': 0, 'forks': 0}
        for repo in repos:
            if repo['private']:
                stats['private'] += 1
            else:
                stats['public'] += 1
                stats['forks'] += repo['forks_count']
        return stats

# Example usage:
# github_stats = GitHubStats('some_username')
# print(github_stats.get_stats())