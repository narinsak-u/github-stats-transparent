import requests

class GitHubStats:
    def __init__(self, token):
        self.token = token

    def query(self, query_str):
        headers = {'Authorization': f'token {self.token}'}
        response = requests.post('https://api.github.com/graphql', json={'query': query_str}, headers=headers)
        
        # Adding HTTP status code checks
        if response.status_code != 200:
            raise Exception(f'Query failed with status code {response.status_code}: {response.text}')  
        
        return response.json()

    def get_stats(self, repository):
        # Better exception handling with informative error messages
        try:
            stats = self.query(f'{{ repository(owner: "{repository.owner}", name: "{repository.name}") {{ stargazers {{ totalCount }} }} }}')
            return stats['data']['repository']['stargazers']['totalCount']
        except Exception as e:
            print(f'Error fetching stats for {repository.name}: {str(e)}')
            return None

    def process_repositories(self, repositories):
        for repo in repositories:
            count = self.get_stats(repo)
            if count is not None:
                print(f'Repo: {repo.name}, Stars: {count}')