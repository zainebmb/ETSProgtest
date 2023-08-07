import requests
import csv

def get_github_issues(owner, repo, num_issues=500):
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {'state': 'all', 'per_page': 100}
    total_issues = []

    while len(total_issues) < num_issues:
        response = requests.get(issues_url, params=params)
        if response.status_code == 200:
            issues = response.json()
            if not issues:
                break
            total_issues += [issue for issue in issues if 'pull_request' not in issue]
            if 'next' in response.links:
                issues_url = response.links['next']['url']
            else:
                break
        else:
            print("Failed to fetch issues.")
            print(response.status_code )
            break

    return total_issues[:num_issues]

def save_issues_to_csv(issues, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Issue Title', 'Issue Number', 'State', 'Created At', 'Updated At','Closed At' ,'URL', 'Labels', 'Author', 'Comments'])

        for issue in issues:
            labels = [label['name'] for label in issue['labels']]
            assignees = [assignee['login'] for assignee in issue['assignees']]
            comments = issue['comments']

            writer.writerow([
                issue['title'],
                issue['number'],
                issue['state'],
                issue['created_at'],
                issue['updated_at'],
                issue['closed_at'],
                issue['html_url'],
                labels,
                issue['user']['login'],
                comments,
            ])

if __name__ == "__main__":
    repo_owner = "rails"  
    repo_name = "rails"  
    csv_file = "issues.csv"  

    issues = get_github_issues(repo_owner, repo_name)
    save_issues_to_csv(issues, csv_file)

    print(f"{len(issues)} issues saved to '{csv_file}'.")
