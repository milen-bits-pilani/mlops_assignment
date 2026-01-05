#!/bin/bash
# Build Docker image, save as tar, and load into kind

set -e

IMAGE_NAME="heart-disease-api"
IMAGE_TAG="latest"
TAR_FILE="${IMAGE_NAME}.tar"
KIND_CLUSTER="local-k8s-1"

echo "=========================================="
echo "Building and Loading Docker Image to Kind"
echo "=========================================="

# Step 1: Build Docker image
echo ""
echo "Step 1: Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -ne 0 ]; then
    echo "Error: Docker build failed"
    exit 1
fi

echo "✓ Docker image built successfully"

# Step 2: Save image as tar
echo ""
echo "Step 2: Saving Docker image to ${TAR_FILE}..."
docker save ${IMAGE_NAME}:${IMAGE_TAG} -o ${TAR_FILE}

if [ $? -ne 0 ]; then
    echo "Error: Failed to save Docker image"
    exit 1
fi

# Get file size
FILE_SIZE=$(du -h ${TAR_FILE} | cut -f1)
echo "✓ Image saved to ${TAR_FILE} (${FILE_SIZE})"

# Step 3: Load image into kind
echo ""
echo "Step 3: Loading image into kind cluster '${KIND_CLUSTER}'..."
sudo kind load image-archive ${TAR_FILE} --name ${KIND_CLUSTER}

if [ $? -ne 0 ]; then
    echo "Error: Failed to load image into kind"
    exit 1
fi

echo "✓ Image loaded into kind successfully"

echo ""
echo "=========================================="
echo "Success! Image is ready in kind cluster"
echo "=========================================="
echo ""
echo "You can now deploy:"
echo "  kubectl apply -f k8s/deployment.yaml"
echo ""
echo "Or copy models to pods:"
echo "  ./scripts/copy_models_to_k8s.sh"

