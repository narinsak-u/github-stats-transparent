import requests

class GitHubStats:
    def __init__(self, token):
        self.token = token

    def query(self, query, variables=None):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Query failed with status code {response.status_code}: {response.text}')  # Add HTTP status code checks
        return response.json()

    def get_stats(self, repos):
        stats = []
        page = 1
        while True:
            for repo in repos:
                try:
                    # Process each repo
                    data = self.query('query { repository(owner: "{owner}", name: "{name}") { stargazers { totalCount } }}', {'owner': repo['owner'], 'name': repo['name']})
                    stats.append({
                        'repo': repo['name'],
                        'stargazers': data['data']['repository']['stargazers']['totalCount']
                    })
                except Exception as e:
                    print(f'Error processing repo {repo['name']}: {str(e)}')  # Improved exception handling
            # Pagination logic here
            if not data['data']['repository']['stargazers']:
                break
            page += 1
        return stats