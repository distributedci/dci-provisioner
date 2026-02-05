#!/bin/bash
set -e
FULL_IMAGE_STRING="$1"
if [ -z "$FULL_IMAGE_STRING" ]; then
    echo "Error: No image argument provided."
    exit 1
fi

REGISTRY_BASE="${FULL_IMAGE_STRING%/*}"
VERSION="${FULL_IMAGE_STRING##*:}"
PROVISIONER_IMAGE="${REGISTRY_BASE}/dci-provisioner:${VERSION}"
LAB_IMAGE="${REGISTRY_BASE}/dci-lab:${VERSION}"

podman build -f Containerfiles/Containerfile-provisioner -t "$PROVISIONER_IMAGE" .

LAB_IMAGE_BUILD_OPTS=""
EXPIRATION=$(grep "LABEL quay.expires-after" Containerfiles/Containerfile-provisioner | cut -d= -f2)

if [ -n "$EXPIRATION" ]; then
    LAB_IMAGE_BUILD_OPTS="--label quay.expires-after=$EXPIRATION"
fi
podman build $LAB_IMAGE_BUILD_OPTS -f Containerfiles/Containerfile-lab -t "$LAB_IMAGE" .
