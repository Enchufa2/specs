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
        for tag in gh.get_repo(repo).get_releases():
            if not (not prerel and tag.prerelease):
                break
        return tag.tag_name.replace('v', '')
    except:
        return '0'

def update_spec(pkg, version):
    cmd = f'sed -i -E "s/(^Version:\\s*).*/\\1{version}/" {pkg}/{pkg}.spec'
    check_output(cmd, shell=True)

def commit_repo(pkg, version):
    r = Repo()
    r.index.add(f'{pkg}/{pkg}.spec')
    r.index.commit(f'{pkg}: update to {version}')
    r.remote().push()

def build_pkg(pkg, proj):
    copr = Client.create_from_config_file()
    user = copr.config['username']
    copr.package_proxy.build(user, proj, pkg)

with open('sync.csv', newline='') as f:
    for pkg, proj, prerel in csv.reader(f, delimiter=' '):
        version_spec = query_spec(pkg, 'version')
        version_repo = query_repo(pkg, prerel == "True").replace('-', '+')
        if Version(version_repo) <= Version(version_spec):
            continue
        update_spec(pkg, version_repo)
        if os.environ.get('CI') is None:
            continue
        commit_repo(pkg, version_repo)
        build_pkg(pkg, proj)
