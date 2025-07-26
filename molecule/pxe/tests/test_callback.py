import pytest
import requests
import json

CALLBACK_HOST = "172.17.0.2"  # Container IP 
CALLBACK_PORT = 5000
CALLBACK_URL = f"http://{CALLBACK_HOST}:{CALLBACK_PORT}"

def test_callback_service_packages_installed(host):
    """Test callback service dependencies are installed"""
    packages = ["python3", "python3-pip", "supervisor"]
    for pkg in packages:
        package = host.package(pkg)
        assert package.is_installed

def test_callback_service_user_exists(host):
    """Test callback service user is created"""
    user = host.user("pxe-callback")
    assert user.exists
    assert user.home == "/opt/pxe-callback"

def test_callback_service_files_exist(host):
    """Test callback service files are deployed"""
    files = [
        "/opt/pxe-callback/app.py",
        "/opt/pxe-callback/config.yml",
        "/etc/supervisor/conf.d/pxe-callback.conf"
    ]
    for file_path in files:
        file_obj = host.file(file_path)
        assert file_obj.exists

def test_supervisor_service_running(host):
    """Test supervisor is running"""
    svc = host.service("supervisor")
    assert svc.is_enabled
    assert svc.is_running

def test_callback_service_listening(host):
    """Test callback service is listening on correct port"""
    socket = host.socket(f"tcp://0.0.0.0:{CALLBACK_PORT}")
    assert socket.is_listening

def test_callback_service_health_endpoint(host):
    """Test callback service health endpoint"""
    try:
        response = requests.get(f"{CALLBACK_URL}/health", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    except requests.exceptions.RequestException:
        pytest.skip("Callback service not reachable from test environment")

def test_post_install_scripts_exist(host):
    """Test post-installation scripts are deployed"""
    scripts = [
        "/var/www/pxe/scripts/post-install.sh",
        "/var/www/pxe/scripts/system-setup.sh",
        "/var/www/pxe/scripts/ssh-keys.sh",
        "/var/www/pxe/scripts/monitoring-agent.sh"
    ]
    for script_path in scripts:
        script = host.file(script_path)
        assert script.exists
        assert script.user == "www-data"
        assert script.mode == 0o755

def test_inventory_directory_exists(host):
    """Test Ansible inventory directory is created"""
    inventory_dir = host.file("/etc/ansible/hosts.d")
    assert inventory_dir.exists
    assert inventory_dir.is_directory

@pytest.mark.integration
def test_node_registration_flow():
    """Integration test: simulate node registration"""
    try:
        # Test data for a fake node registration
        test_node = {
            "hostname": "test-node-01",
            "mac_address": "02:42:ac:11:00:99",
            "ip_address": "172.17.0.99",
            "architecture": "amd64",
            "os_version": "Ubuntu 24.04 LTS",
            "installation_id": "test-install-12345",
            "hardware_info": {
                "cpu_cores": "4",
                "memory_gb": "8",
                "disk_gb": "100"
            }
        }
        
        # Register the test node
        response = requests.post(
            f"{CALLBACK_URL}/register",
            json=test_node,
            timeout=10
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "test-node-01" in data["message"]
        
        # Verify node appears in nodes list
        response = requests.get(f"{CALLBACK_URL}/nodes", timeout=10)
        assert response.status_code == 200
        
        nodes_data = response.json()
        node_hostnames = [node["hostname"] for node in nodes_data["nodes"]]
        assert "test-node-01" in node_hostnames
        
    except requests.exceptions.RequestException:
        pytest.skip("Callback service not reachable for integration test")
