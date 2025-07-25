#!/bin/bash
# VM creation helper script

set -euo pipefail

VM_NAME="${1:-test-vm}"
RAM="${2:-1024}"
DISK="${3:-10G}"

echo "Creating VM: $VM_NAME with ${RAM}MB RAM and ${DISK} disk..."

virt-install \
    --name "$VM_NAME" \
    --ram "$RAM" \
    --disk size=${DISK%G} \
    --vcpus 1 \
    --os-type linux \
    --network bridge=virbr0 \
    --graphics none \
    --console pty,target_type=serial \
    --location 'http://ftp.ubuntu.com/ubuntu/dists/jammy/main/installer-amd64/' \
    --extra-args 'console=ttyS0,115200n8 serial'

echo "VM $VM_NAME created successfully!"
