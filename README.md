## PXE Network Boot Infrastructure

The `pxe` role provides a bare-metal provisioning system for automated network booting and OS installation. It deploys and configures:

- **DHCP Server** (Kea) - Provides IP addresses and PXE boot options to client machines
- **TFTP Server** - Serves initial boot files including netboot.xyz and custom iPXE scripts
- **HTTP Server** (Nginx) - Hosts Ubuntu kernels, initrds, and autoinstall configurations
- **iPXE Boot Menus** - Architecture-aware boot scripts with conditional logic for x86_64 and ARM64 devices
- **Post-Installation Callback System** - FastAPI service that automatically registers newly provisioned nodes into Ansible inventory

The system supports unattended installation of Ubuntu Server 24.04 LTS on both traditional x86_64 systems and ARM64 Raspberry Pi devices. After installation, nodes automatically execute post-installation scripts and report back to the PXE server for integration into your infrastructure automation pipeline.

**Testing**: Includes comprehensive Molecule test suite covering all components and end-to-end functionality.
