#!/bin/bash -e

function print_help {
  cat << \EOF
This script helps you with checking out all repositories for local development.
Usage: setup.sh [-h|--help] [-r|--remotes NAME] [repo] ...

Arguments:

  -h|--help            Print this help
  -r|--remotes NAME    Add remote "fork" ("NAME" is Gitlab user) to all repos
  repo ...             Work only on specified repositories
                       (works on all repositories by default)
EOF
}

repos=""
remotes=""

while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -h|--help)
      print_help
      exit 0
      ;;
    -r|--remotes)
      remotes=$2
      shift
      ;;
    *)
      repos="$key $repos"
      ;;
  esac
  shift
done

if [[ -z "$repos" ]]; then
  repos="worker server jobs pgbouncer data-model"
fi

for repo in $repos; do
  if ! `ls $repo &>/dev/null`; then
    git clone "git@gitlab.cee.redhat.com:bayesian/${repo}.git"
    if [[ $repo == "worker" ]]; then
      curl -O https://gitlab.cee.redhat.com/bayesian/secrets/raw/master/secrets.yaml
      mv secrets.yaml worker/hack/
    fi
  fi
  if [[ -n "$remotes" ]]; then
    pushd $repo &>/dev/null
    if ! `git remote show | grep "^fork$" &>/dev/null`; then
      git remote add fork "git@gitlab.cee.redhat.com:${remotes}/${repo}.git"
    fi
    popd &>/dev/null
  fi
done

echo "Setup done. To run the system locally, run:"
echo "docker-compose up"
