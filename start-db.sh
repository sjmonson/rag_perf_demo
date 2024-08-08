#!/bin/sh

podman volume create --ignore pg_vector_data

exec podman run -d --rm \
  -e POSTGRES_DB=vector -e POSTGRES_PASSWORD=postgres \
  -v pg_vector_data:/var/lib/postgresql/data:Z -p 127.0.0.1:5432:5432 \
  --name pg_vector docker.io/pgvector/pgvector:pg16
