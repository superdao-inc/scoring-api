#!/bin/sh

set -e

exec uvicorn app.main:rest --host 0.0.0.0 --port 8080