import pytest

HTTP_ROOT = "/var/www/pxe"
NGINX_CONFIG = "/etc/nginx/sites-available/pxe"

def test_nginx_package_installed(host):
    pkg = host.package("nginx")
    assert pkg.is_installed

def test_nginx_service_running(host):
    svc = host.service("nginx")
    assert svc.is_enabled
    assert svc.is_running

def test_pxe_http_root_exists(host):
    http_dir = host.file(HTTP_ROOT)
    assert http_dir.exists
    assert http_dir.is_directory
    assert http_dir.user == "www-data"

def test_nginx_pxe_config(host):
    config = host.file(NGINX_CONFIG)
    assert config.exists
    assert f"root {HTTP_ROOT};" in config.content_string

def test_nginx_listening(host):
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening

@pytest.mark.parametrize("subdir", [
    "ubuntu",
    "cloud-init", 
    "preseed",
    "scripts"
])
def test_http_subdirectories(host, subdir):
    path = host.file(f"{HTTP_ROOT}/{subdir}")
    assert path.exists
    assert path.is_directory
    assert path.user == "www-data"
