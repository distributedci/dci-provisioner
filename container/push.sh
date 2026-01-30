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

podman push "$PROVISIONER_IMAGE"
podman push "$LAB_IMAGE"
