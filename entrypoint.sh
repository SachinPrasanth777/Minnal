#!/bin/sh

prisma migrate dev --name init

prisma generate

exec "$@"
