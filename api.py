import requests
import json
import os
from collections import Counter
from collections import OrderedDict
from TOKEN import bearer_token  

headers = {"Authorization": bearer_token}


# github GraphQL query to get data about pinned repos
query_repos = """
{
  repositoryOwner(login: "Ligh7bringer") {
    ... on User {
      pinnedItems(first: 6) {
        edges {
          node {
            __typename
            ... on Repository {
              name
              description
              url
              languages(first: 5) {
                nodes {
                  name
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

query_langs = """
{
  user(login: "Ligh7bringer") {
    repositories(first: 100) {
      edges {
        node {
          languages(first: 100) {
            nodes {
              name
            }
          }
        }
      }
    }
  }
}
"""

query_repo_count = """
{
  user(login: "Ligh7bringer") {
    id
    name
    url
    repositories(first: 100) {
      totalCount
    }
  }
}
"""


def count_langs(data):
  result = {}
  for k in data:    
    if 'name' in k:
      result[k['name']] = result.get(k['name'], 0) + 1

  return result


# sends a request with the requests library
def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


if __name__ == "__main__":
  # get pinned repos
  result_repos = run_query(query_repos)
  with open('data/projects.json', 'w') as outfile:  
      json.dump(result_repos, outfile, sort_keys=True, indent=4, separators=(',', ': '))

  # get most used languages
  result_langs = run_query(query_langs)
  formatted = []
  for k in result_langs['data']['user']['repositories']['edges']:
    formatted.extend(k['node']['languages']['nodes'])
  count = count_langs(formatted)

  final = []
  for i in count:
    tmp = {}
    tmp["name"] = i
    tmp["used"] = count[i]
    final.append(tmp)
    
  with open('data/languages.json', 'w') as outfile:  
      json.dump(final, outfile, indent=4, separators=(',', ': '))

  # get the total count of my repositories
  result_repo_count = run_query(query_repo_count)
  with open('data/repoCount.json', 'w') as outfile:  
    json.dump(result_repo_count['data']['user']['repositories'], outfile, indent=4, separators=(',', ': '))