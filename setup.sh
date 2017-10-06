#!/bin/bash -e

function print_help {
  cat << \EOF
This script helps you with checking out all repositories for local development.
Usage: setup.sh [-h|--help] [-r|--remotes NAME] [repo] ...

Arguments:

  -h|--help            Print this help
  -r|--remotes NAME    Add remote "fork" ("NAME" is a GitHub user) to all repos
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
  repos="worker server jobs pgbouncer data-model stack-analysis firehose-fetcher scaler recommender"
fi

for repo in $repos; do
  fullrepo=fabric8-analytics-${repo}
  if ! `ls $fullrepo &>/dev/null`; then
    git clone "git@github.com:fabric8-analytics/${fullrepo}.git"
    if [[ $repo == "worker" ]]; then
      cat > ${fullrepo}/hack/secrets.yaml << \EOF
pulp:
  # url: "https://pulp.com"
  # username: "user"
  # password: "password"
github:
  # Generate your token at https://github.com/settings/tokens
  # token: "123456asdf"
bigquery:
  # token: 'mysecrettokentobigquery'
EOF
      echo "Dummy worker/hack/secrets.yaml created. Modify it as necessary."
    fi
  fi

  if [[ -n "$remotes" ]]; then
    pushd $fullrepo &>/dev/null
    if ! `git remote show | grep "^fork$" &>/dev/null`; then
      git remote add fork "git@github.com:${remotes}/${fullrepo}.git"
    fi
    popd &>/dev/null
  fi
done

echo "Setup done. To run the system locally, run:"
echo "docker-compose up"
echo "If you want to mount source code inside the containers, run:"
echo "./docker-compose.sh up"
