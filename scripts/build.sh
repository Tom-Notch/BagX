#!/bin/sh

docker build -t $USER/bagx:1.0 - < $(dirname "$0")/../Dockerfile
