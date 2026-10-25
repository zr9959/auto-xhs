#!/bin/bash
# Set up the environment in one go: first check what's missing, then download third-party libraries, then prepare your config file.
# What's already set up stays yours: if config.yaml exists, it is never overwritten.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Step 1: check what's missing from the environment"
if ! bash scripts/check-env.sh; then
  echo "Install everything marked 'missing' above first, then run this script again. Later steps wait."
  exit 1
fi

echo
echo "Step 2: download third-party libraries"
if ! bash scripts/fetch-vendor.sh; then
  echo "The libraries didn't download — the output above says where it stuck. Fix it and run this script again; earlier steps won't be wasted."
  exit 1
fi

echo
echo "Step 3: prepare the config file"
if [ -f config.yaml ]; then
  echo "config.yaml already exists — left untouched."
elif [ -f config.example.yaml ]; then
  cp config.example.yaml config.yaml
  echo "Copied config.example.yaml to config.yaml — edit that copy."
else
  echo "config.example.yaml not found — skipping this step. Once the repo has an example config, copy it and name it config.yaml yourself."
fi

echo
echo "All set. Next, in this order:"
echo "  1. Open SETUP.md and fill in config.yaml item by item. What each item does and what's recommended is all there."
echo "  2. For the automation level item, pick one before continuing: full-auto, look-before-publishing, or drafts-only. You can change it later — no need to decide once and for all."
echo "  3. Xiaohongshu login can only be done by you scanning the QR code — the steps are in SETUP.md. Before that's set up, run through the flow once with the fictional example in examples/."
