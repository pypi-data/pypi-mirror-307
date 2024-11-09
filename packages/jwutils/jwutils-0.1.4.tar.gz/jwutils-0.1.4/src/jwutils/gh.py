import requests


def gh2local(user, repo, branch, filepath):
    try:
        url = f"https://raw.githubusercontent.com/{user}/{repo}/refs/heads/{branch}/{filepath}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for a bad response
        filename = filepath.split("/")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
