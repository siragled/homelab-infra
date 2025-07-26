import pytest

HTTP_ROOT = "/var/www/pxe"

def test_ipxe_boot_script_exists(host):
    boot_script = host.file(f"{HTTP_ROOT}/boot.ipxe")
    assert boot_script.exists
    assert boot_script.user == "www-data"
    # Update assertion to match actual content
    content = boot_script.content_string
    assert "PXE Boot Menu" in content
    assert "Architecture detection" in content

@pytest.mark.parametrize("arch", ["amd64", "arm64"])
def test_arch_specific_ipxe_scripts(host, arch):
    script = host.file(f"{HTTP_ROOT}/ipxe/boot-{arch}.ipxe")
    assert script.exists
    assert script.user == "www-data"
    # Check for iPXE-specific content
    content = script.content_string
    assert "#!ipxe" in content
    assert "menu" in content

def test_autoinstall_files_exist(host):
    """Test autoinstall user-data files exist (replaces preseed test)"""
    user_data_amd64 = host.file(f"{HTTP_ROOT}/cloud-init/user-data")
    user_data_arm64 = host.file(f"{HTTP_ROOT}/cloud-init/user-data-arm64")
    
    assert user_data_amd64.exists
    assert user_data_arm64.exists
    assert user_data_amd64.user == "www-data"
    assert user_data_arm64.user == "www-data"
    
    # Check they contain autoinstall configuration
    assert "#cloud-config" in user_data_amd64.content_string
    assert "autoinstall:" in user_data_amd64.content_string
    assert "#cloud-config" in user_data_arm64.content_string
    assert "autoinstall:" in user_data_arm64.content_string

def test_meta_data_files_exist(host):
    """Test meta-data files for cloud-init"""
    meta_data = host.file(f"{HTTP_ROOT}/cloud-init/meta-data")
    meta_data_arm64 = host.file(f"{HTTP_ROOT}/cloud-init/meta-data-arm64")
    
    assert meta_data.exists
    assert meta_data_arm64.exists
    assert meta_data.user == "www-data"
    assert meta_data_arm64.user == "www-data"
    
    # Check they contain expected instance-id
    assert "ubuntu-pxe-default" in meta_data.content_string
    assert "ubuntu-pxe-default" in meta_data_arm64.content_string

def test_ipxe_scripts_are_valid(host):
    boot_script = host.file(f"{HTTP_ROOT}/boot.ipxe")
    content = boot_script.content_string
    
    # Check for iPXE shebang
    assert content.startswith("#!ipxe")
    
    # Check for basic iPXE commands
    assert "chain" in content
    assert "echo" in content
    assert "goto" in content

def test_cloud_init_directory_structure(host):
    """Test that cloud-init directory has proper structure"""
    cloud_init_dir = host.file(f"{HTTP_ROOT}/cloud-init")
    assert cloud_init_dir.exists
    assert cloud_init_dir.is_directory
    assert cloud_init_dir.user == "www-data"
