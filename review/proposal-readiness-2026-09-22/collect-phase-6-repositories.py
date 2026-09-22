#!/usr/bin/env python3
"""Collect public GitHub figures, preserving request dates and counting scopes."""
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent
requests = []

def get(endpoint):
    started = dt.datetime.now(dt.timezone.utc)
    raw = subprocess.check_output(['gh', 'api', '--method', 'GET', '--include', endpoint], text=True)
    headers, body = raw.split('\n\n', 1)
    data = json.loads(body)
    requests.append({'endpoint': 'https://api.github.com/' + endpoint,
                     'collected_at_utc': started.isoformat(),
                     'collected_at_vienna': started.astimezone(ZoneInfo('Europe/Vienna')).isoformat(),
                     'response_headers': headers})
    return data, headers

def paginated(endpoint):
    rows = []; page = 1
    while True:
        data, headers = get(endpoint + f'?per_page=100&page={page}')
        rows.extend(data)
        if 'rel="next"' not in headers: return rows
        page += 1

repos = []
for name in ['SNodeC/snode.c', 'SNodeC/mqttsuite']:
    endpoint = f'repos/{name}'
    repo, _ = get(endpoint)
    head, _ = get(endpoint + '/commits/' + repo['default_branch'])
    sha = head['sha']
    commits, headers = get(endpoint + f'/commits?sha={sha}&per_page=1')
    last = re.search(r'<([^>]+)>; rel="last"', headers)
    count = int(re.search(r'[?&]page=(\d+)', last[1])[1]) if last else len(commits)
    oldest, _ = get(last[1].removeprefix('https://api.github.com/')) if last else (commits, '')
    commit = oldest[0]
    releases = paginated(endpoint + '/releases')
    tags = paginated(endpoint + '/tags')
    contributors = paginated(endpoint + '/contributors')
    repos.append({
        'repository': name, 'url': repo['html_url'], 'default_branch': repo['default_branch'],
        'counted_head': sha, 'reachable_commits': count,
        'stars': repo['stargazers_count'], 'forks': repo['forks_count'],
        'watching_subscribers': repo['subscribers_count'],
        'oldest_api_commit': {'sha': commit['sha'], 'author_date': commit['commit']['author']['date'],
                              'committer_date': commit['commit']['committer']['date'],
                              'parent_count': len(commit['parents']), 'url': commit['html_url']},
        'releases': [{k: r[k] for k in ['tag_name','published_at','draft','prerelease','html_url']} for r in releases],
        'tags': [r['name'] for r in tags],
        'contributors': [{k: r[k] for k in ['login','type','contributions','html_url']} for r in contributors],
    })
result = {'method': 'Live GitHub REST API via gh api; no local checkout used. Commit count is the last page number with per_page=1 at a captured default-branch head. The oldest API entry is reported with its parent count; this is not a search over all branches. Contributor, release and tag endpoints are paginated to exhaustion. Contributors omit anonymous identities (GitHub default); account type User is not independent proof of a unique human. Subscriber count is subscribers_count, not watchers_count (which aliases stars). Counts are endpoint snapshots, not simultaneous or measures of users, deployments, downloads or book buyers.',
          'repositories': repos, 'requests': requests}
(OUT / 'phase-6-repository-figures.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'repositories': repos, 'first_collection': requests[0]['collected_at_vienna'],
                  'last_collection': requests[-1]['collected_at_vienna']}, indent=2))
