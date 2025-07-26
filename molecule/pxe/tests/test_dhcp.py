import json
import pytest

CFG_PATH = "/etc/kea/kea-dhcp4.conf"

def test_kea_package_installed(host):
    pkg = host.package("kea-dhcp4-server")
    assert pkg.is_installed

def test_kea_service_running(host):
    svc = host.service("kea-dhcp4-server")
    assert svc.is_enabled
    assert svc.is_running

def test_config_is_valid_json(host):
    cfg = host.file(CFG_PATH)
    assert cfg.exists
    # Parse JSON to ensure it's valid
    config_data = json.loads(cfg.content_string)
    assert "Dhcp4" in config_data

def test_dhcp_config_structure(host):
    """Test that the Kea config has expected structure and values"""
    cfg = host.file(CFG_PATH)
    config_data = json.loads(cfg.content_string)
    
    dhcp4 = config_data["Dhcp4"]
    
    # Check lease database
    assert dhcp4["lease-database"]["type"] == "memfile"
    
    # Check we have subnets
    assert "subnet4" in dhcp4
    assert len(dhcp4["subnet4"]) > 0
    
    subnet = dhcp4["subnet4"][0]
    assert subnet["subnet"] == "192.168.1.0/24"

def test_pxe_boot_config(host):
    """Test PXE boot configuration"""
    cfg = host.file(CFG_PATH)
    config_data = json.loads(cfg.content_string)
    
    subnet = config_data["Dhcp4"]["subnet4"][0]
    
    # Check if using Kea's built-in PXE fields
    if "next-server" in subnet:
        assert subnet["next-server"] is not None
        assert "boot-file-name" in subnet
        assert subnet["boot-file-name"] == "netboot.xyz.kpxe" 

def test_global_options(host):
    """Test global DHCP options"""
    cfg = host.file(CFG_PATH)
    config_data = json.loads(cfg.content_string)
    
    global_options = {opt["name"]: opt["data"] for opt in config_data["Dhcp4"]["option-data"]}
    
    assert "domain-name-servers" in global_options
    assert "domain-name" in global_options
    assert global_options["domain-name"] == "homelab.local"
