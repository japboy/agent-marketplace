#!/bin/sh

set -eu

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/../.." && pwd)
positive_output=$(mktemp "${TMPDIR:-/tmp}/agent-marketplace-vale-positive.XXXXXX")
positive_sorted=$(mktemp "${TMPDIR:-/tmp}/agent-marketplace-vale-positive-sorted.XXXXXX")
positive_stderr=$(mktemp "${TMPDIR:-/tmp}/agent-marketplace-vale-positive-stderr.XXXXXX")
negative_output=$(mktemp "${TMPDIR:-/tmp}/agent-marketplace-vale-negative.XXXXXX")
negative_stderr=$(mktemp "${TMPDIR:-/tmp}/agent-marketplace-vale-negative-stderr.XXXXXX")

cleanup() {
  rm -f "$positive_output" "$positive_sorted" "$positive_stderr" "$negative_output" "$negative_stderr"
}
trap cleanup EXIT HUP INT TERM

cd "$repo_root"

set +e
mise exec -- vale --no-global --config=.vale.ini --output=line \
  tests/vale/fixtures/positive.md >"$positive_output" 2>"$positive_stderr"
positive_status=$?
set -e

if [ "$positive_status" -ne 1 ] || [ -s "$positive_stderr" ]; then
  printf 'positive Vale fixture returned exit %s; expected 1\n' "$positive_status" >&2
  cat "$positive_output" "$positive_stderr" >&2
  exit 1
fi

LC_ALL=C sort "$positive_output" >"$positive_sorted"
diff -u tests/vale/fixtures/positive.expected "$positive_sorted"

set +e
mise exec -- vale --no-global --config=.vale.ini --output=line \
  tests/vale/fixtures/negative.md >"$negative_output" 2>"$negative_stderr"
negative_status=$?
set -e

if [ "$negative_status" -ne 0 ] || [ -s "$negative_output" ] || [ -s "$negative_stderr" ]; then
  printf 'negative Vale fixture returned exit %s with unexpected output; expected 0 and no alerts\n' \
    "$negative_status" >&2
  cat "$negative_output" "$negative_stderr" >&2
  exit 1
fi

printf '%s\n' 'Vale fixtures passed: 3 visible-boundary errors; code and URL scopes ignored'
