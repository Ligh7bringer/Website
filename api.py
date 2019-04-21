import requests
import json
import os
from TOKEN import bearer_token

headers = {"Authorization": bearer_token}


# sends a request with the requests library
def run_query(query):
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# github GraphQL query to get data about pinned repos
query = """
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

result = run_query(query)

with open('data/projects.json', 'w') as outfile:  
    json.dump(result, outfile, sort_keys=True, indent=4, separators=(',', ': '))