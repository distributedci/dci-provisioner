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
podman build -f Containerfiles/Containerfile-lab -t "$LAB_IMAGE" .
