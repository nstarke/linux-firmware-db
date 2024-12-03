#!/bin/sh
cd ..
git add .
git commit -m "$LATEST_TAG"
git push origin main