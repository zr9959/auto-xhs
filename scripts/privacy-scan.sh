#!/bin/bash
# Before publishing, scan the repo yourself for things that shouldn't be in it.
# Three scans: secrets, the private words you put in the local wordlist, hardcoded local paths.
# The local wordlist is privacy-denylist.local.txt, in the repo root, one word per line.
# That file itself is in .gitignore and never enters the repo — the words in it are exactly the ones
# that must stay private; if it got committed, the whole scan would be pointless.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0

echo "1. Scan for secrets (gitleaks)"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks detect --source . --config .gitleaks.toml --no-banner; then
    echo "gitleaks finished, no secrets found."
  else
    echo "gitleaks flagged something — see the list above, fix it, then scan again."
    FAIL=1
  fi
else
  echo "gitleaks not found on this machine — skipping this item. Before publishing, re-scan on a machine that has gitleaks."
fi

echo
echo "2. Scan for private words (local wordlist)"
if [ -f privacy-denylist.local.txt ]; then
  while IFS= read -r word; do
    [ -z "$word" ] && continue
    case "$word" in \#*) continue;; esac
    hits=$(grep -rn --exclude-dir=.git --exclude-dir=data --exclude=privacy-denylist.local.txt -F "$word" . 2>/dev/null | wc -l)
    if [ "$hits" -gt 0 ]; then
      echo "The word \"$word\" appears $hits times in the repo — remove them before publishing."
      FAIL=1
    fi
  done < privacy-denylist.local.txt
  echo "Wordlist scan done."
else
  echo "No privacy-denylist.local.txt — skipping this item."
  echo "Before publishing, write your own account names, account IDs, emails, and similar words into that file, one per line, then run again."
fi

echo
echo "3. Scan for hardcoded local paths"
hits=$(grep -rn --exclude-dir=.git --exclude-dir=data -E "/home/[a-z]+/|/Users/[a-z]+/" . 2>/dev/null | grep -v "privacy-scan.sh" | wc -l)
if [ "$hits" -gt 0 ]; then
  grep -rn --exclude-dir=.git --exclude-dir=data -E "/home/[a-z]+/|/Users/[a-z]+/" . 2>/dev/null | grep -v "privacy-scan.sh" | head -10
  echo "These are hardcoded local paths — change them to relative paths or config entries before publishing."
  FAIL=1
else
  echo "No hardcoded local paths."
fi

echo
if [ "$FAIL" -eq 0 ]; then
  echo "Scan done, no problems found. Finally, read through the README, examples, and code comments by hand — those three places hide real information most easily."
else
  echo "Problems found — fix them, then run this script again."
  exit 1
fi
