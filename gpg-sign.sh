#!/bin/bash

for filename in dist/*
do
  gpg --detach-sign $filename
  gpg --verify $filename.sig $filename
done;

leetscraper=src/leetscraper/leetscraper.py
gpg --detach-sign $leetscraper
gpg --verify $leetscraper.sig $leetscraper