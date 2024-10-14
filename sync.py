#!/usr/bin/python3

import csv, os
from subprocess import check_output
from packaging.version import Version
from github import Github
from git import Repo
from copr.v3 import Client

def query_spec(pkg, tag):
    cmd = f'rpmspec -q {pkg}/{pkg}.spec --qf "%{{{tag}}}\n" | tail -n1'
    return check_output(cmd, shell=True).decode('utf-8').strip()

def query_repo(pkg, prerel):
    gh = Github()
    repo = query_spec(pkg, 'url').split('github.com/')[1]
    try:
        repo = gh.get_repo(repo)
        if prerel:
            ver = repo.get_tags()[0].name
            if 'daily' in ver: # positron publishes latest+daily
                ver = repo.get_tags()[1].name
        else:
            for tag in repo.get_releases():
                if not tag.prerelease:
                    break
            ver = tag.tag_name
        return ver.replace('v', '')
    except:
        return '0'

def create_issue(pkg, version):
    cmd = f'gh issue create -t "{pkg}: version {version} is available" -b ""'
    check_output(cmd, shell=True)
    print(f'{pkg}: issue created')

def update_spec(pkg, version):
    cmd = f'sed -i -E "s/(^Version:\\s*).*/\\1{version}/" {pkg}/{pkg}.spec'
    check_output(cmd, shell=True)
    print(f'{pkg}: spec updated')

def commit_repo(pkg, version):
    r = Repo()
    r.index.add(f'{pkg}/{pkg}.spec')
    r.index.commit(f'{pkg}: update to {version}')
    r.remote().push()
    print(f'{pkg}: committed')

def build_pkg(pkg, proj):
    copr = Client.create_from_config_file()
    user = copr.config['username']
    copr.package_proxy.build(user, proj, pkg)
    print(f'{pkg}: new build started')

with open('sync.csv', newline='') as f:
    for pkg, proj, prerel, build in csv.reader(f, delimiter=' '):
        version_spec = query_spec(pkg, 'version')
        version_repo = query_repo(pkg, prerel == "True").replace('-', '+')
        print(f'{pkg}: spec {version_spec} | repo {version_repo}')
        if Version(version_repo) <= Version(version_spec):
            continue
        if not build:
            create_issue(pkg, version_repo)
            continue
        update_spec(pkg, version_repo)
        if os.environ.get('CI') is None:
            continue
        commit_repo(pkg, version_repo)
        build_pkg(pkg, proj)
