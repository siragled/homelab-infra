import pytest

TFTP_ROOT = "/srv/tftp"
TFTP_CONFIG = "/etc/default/tftpd-hpa"

def test_tftp_package_installed(host):
    pkg = host.package("tftpd-hpa")
    assert pkg.is_installed

def test_tftp_service_running(host):
    svc = host.service("tftpd-hpa")
    assert svc.is_enabled
    assert svc.is_running

def test_tftp_root_exists(host):
    tftp_dir = host.file(TFTP_ROOT)
    assert tftp_dir.exists
    assert tftp_dir.is_directory
    assert tftp_dir.user == "tftp"
    assert tftp_dir.group == "tftp"

def test_tftp_config_file(host):
    config = host.file(TFTP_CONFIG)
    assert config.exists
    assert f'TFTP_DIRECTORY="{TFTP_ROOT}"' in config.content_string
    assert 'TFTP_ADDRESS="0.0.0.0:69"' in config.content_string

@pytest.mark.parametrize("binary", [
    "netboot.xyz.kpxe",
    "netboot.xyz.efi"
])
def test_netboot_binaries_present(host, binary):
    path = host.file(f"{TFTP_ROOT}/{binary}")
    assert path.exists
    assert path.user == "tftp"
    assert path.size > 50000  # Reasonable size check

def test_tftp_port_listening(host):
    # Check that TFTP is listening on port 69
    socket = host.socket("udp://0.0.0.0:69")
    assert socket.is_listening

@pytest.mark.parametrize("binary", [
    "netboot.xyz.kpxe",
    "netboot.xyz.efi"
])
def test_netboot_binaries_downloaded(host, binary):
    """Test netboot.xyz binaries are downloaded and properly configured"""
    path = host.file(f"{TFTP_ROOT}/{binary}")
    assert path.exists
    assert path.user == "tftp"
    assert path.group == "tftp" 
    assert path.mode == 0o644
