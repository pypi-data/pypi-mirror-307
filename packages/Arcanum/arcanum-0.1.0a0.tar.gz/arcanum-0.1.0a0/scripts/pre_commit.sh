#!/usr/bin/env bash

HOOK_TYPES=("pre-commit" "commit-msg" "pre-push")

is_hook_installed() {
  local hook_type=$1
  [[ -f ".git/hooks/${hook_type}" ]] &&
    grep -q "pre-commit" ".git/hooks/${hook_type}"
}

main() {
  for hook_type in "${HOOK_TYPES[@]}"; do
    if ! is_hook_installed "$hook_type"; then
      echo "Installing '${hook_type}' hook..."
      if [[ "$hook_type" == "pre-commit" ]]; then
        pre-commit install
      else
        pre-commit install --hook-type "$hook_type"
      fi
    else
      echo "'${hook_type}' hook already installed"
    fi
  done
}

if [[ "$#" -eq 1 && "$1" == *"up"* ]]; then
  pre-commit autoupdate && main
else main; fi
