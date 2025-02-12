import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
import os

def check_github_repo(owner, repo, token=None):
    """
    Description:
    -----------
    Checks to confirm that a GitHub repository exists.

    Parameters:
    ----------
    owner: String
           The owner (username or organization) of the repository.
    repo: String
          The name of the GitHub repository.
    token: String (optional)
           GitHub personal access token for authentication.
    """
    # GitHub API endpoint for repository details
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    # Headers for the request
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        # Make the GET request to the GitHub API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # If the repository exists
        print(f"GitHub Repository: {owner}/{repo} [\u2714]")
    except HTTPError as e:
        # Handle errors (e.g., repository not found)
        if response.status_code == 404:
            print(f"GitHub Repository: {owner}/{repo} [X]")
            print("Error Reason: Repository not found.")
        else:
            print(f"GitHub Repository: {owner}/{repo} [X]")
            print(f"Error Reason: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your GitHub owner and repository name
    owner = "jesvin1"
    repo = "AWS_Sagemaker_Assignment_V01"
    # Load environment variables from .env file
    load_dotenv()

    # Access the GITHUB_TOKEN environment variable
    github_token = os.getenv("GITHUB_TOKEN")
    # Optional: Replace with your GitHub personal access token
    token = github_token
    check_github_repo(owner, repo, token)