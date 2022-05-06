#!/bin/bash

for filename in dist/*
do
  gpg --detach-sign $filename
  gpg --verify $filename.sig $filename
done;
