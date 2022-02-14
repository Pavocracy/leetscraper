#!/bin/bash

leetscraper=src/leetscraper/leetscraper.py
gpg --detach-sign $leetscraper
gpg --verify $leetscraper.sig $leetscraper