import logging
import os
from pathlib import Path

from mtmai.core.config import settings
from mtmlib.env import is_ubuntu
from mtmlib.mtutils import bash

logger = logging.getLogger()


def install_kasmvnc():
    # 安装依赖
    if is_ubuntu():
        bash("""
        wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.0g-2ubuntu4_amd64.deb && \
        sudo dpkg -i ./libssl1.1_1.1.0g-2ubuntu4_amd64.deb && \
        sudo rm ./libssl1.1_1.1.0g-2ubuntu4_amd64.deb
        """)

    # debian https://github.com/kasmtech/KasmVNC/releases/download/v1.3.1/kasmvncserver_bullseye_1.3.1_amd64.deb
    # ubuntu https://github.com/kasmtech/KasmVNC/releases/download/v1.3.1/kasmvncserver_jammy_1.3.1_amd64.deb
    bash("""
    curl -sSL -o /tmp/kasmvncserver.deb https://github.com/kasmtech/KasmVNC/releases/download/v1.3.1/kasmvncserver_bullseye_1.3.1_amd64.deb && \
    sudo apt install -y /tmp/kasmvncserver.deb && \
    rm -rdf /tmp/kasmvncserver.deb && \
    mkdir ${HOME}/.certs -p && \
    mkdir ${HOME}/.vnc -p && \

    sudo openssl req -subj '/CN=example.com/O=My Company Name LTD./C=US' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/private/ssl-cert-snakeoil.pem
    """)

    import os

    nonroot_user = os.environ.get("NONROOT_USER")
    if nonroot_user:
        bash(f"sudo adduser {nonroot_user} ssl-cert")
    else:
        logger.warning(
            "NONROOT_USER environment variable not set. Skipping adding user to ssl-cert group."
        )

    # Install desktop components
    bash("""
    echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections
    sudo apt-get update -yqq
    DEBIAN_FRONTEND=noninteractive sudo apt install -yqq debconf-utils
    DEBIAN_FRONTEND=noninteractive sudo apt-get install -yqq keyboard-configuration
    DEBIAN_FRONTEND=noninteractive sudo apt install -yqq --no-install-recommends \
        dbus-x11 \
        locales \
        pavucontrol \
        pulseaudio \
        pulseaudio-utils \
        x11-xserver-utils \
        xfce4 \
        xfce4-goodies \
        xfce4-pulseaudio-plugin""")

    bash("""
    sudo apt update -yqq
    DEBIAN_FRONTEND=noninteractive sudo apt install -yqq --no-install-recommends \
        pciutils \
        bash-completion \
        xorg xrdp dbus \
        x11-xserver-utils \
        xdg-utils \
        fbautostart \
        at-spi2-core \
        xterm \
        eterm \
        tilix


    DEBIAN_FRONTEND=noninteractive sudo apt install -yqq --no-install-recommends \
        libswitch-perl \
        libtry-tiny-perl \
        libyaml-tiny-perl \
        libhash-merge-simple-perl \
        liblist-moreutils-perl \
        libdatetime-perl \
        libdatetime-timezone-perl

    DEBIAN_FRONTEND=noninteractive sudo apt install -yqq --no-install-recommends \
        xfonts-intl-chinese ttf-wqy-microhei xfonts-intl-chinese xfonts-wqy

    """)


def run_kasmvnc():
    import shutil
    import subprocess
    import time

    if not shutil.which("vncpasswd"):
        logger.info("vncpasswd command not found. Installing KasmVNC...")
        install_kasmvnc()
    else:
        logger.info("vncpasswd command found. Skipping KasmVNC installation.")
    logger.info("start_kasmvnc")
    home = Path.home()
    DEFAULT_PASSWORD = settings.DEFAULT_PASSWORD
    try:
        user = os.getlogin()  # Try to get the current logged-in user
    except OSError:
        # Fallback to using environment variable or a default value
        user = os.environ.get("USER", "default_user")
    bash(f"mkdir -p {home}/.certs/")
    bash(f"mkdir -p {home}/.vnc/")
    bash(
        f"openssl req -subj '/CN=example.com/O=My Company Name LTD./C=US' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout {home}/.certs/ssl-cert-snakeoil.key -out {home}/.certs/ssl-cert-snakeoil.pem"
    )
    # 将会输出到文件 ~/.vnc/passwd
    bash(f'echo "{DEFAULT_PASSWORD}\n{DEFAULT_PASSWORD}\n" | vncpasswd -u {user} -r -w')
    bash(
        f'echo "{DEFAULT_PASSWORD}\n{DEFAULT_PASSWORD}\n" | vncpasswd -u {user} -r -w ~/.kasmpasswd'
    )

    setting_content = f"""
logging:
    log_writer_name: all
    log_dest: logfile
    level: 100
network:
    protocol: http
    interface: 0.0.0.0
    websocket_port: auto
    use_ipv4: true
    use_ipv6: true
    ssl:
        require_ssl: false
        pem_certificate: {home}/.certs/ssl-cert-snakeoil.pem
        pem_key: {home}/.certs/ssl-cert-snakeoil.key
"""
    Path(f"{home}/.vnc/kasmvnc.yaml").write_text(setting_content)
    Path(f"{home}/.vnc/xstartup").write_text("""#!/bin/sh
set -x
xfce4-terminal &
exec xfce4-session
""")
    bash(f"chmod 755 {home}/.vnc/xstartup")
    bash("touch ~/.vnc/.de-was-selected")
    bash("vncserver -kill :1 || true")

    # 使用subprocess.Popen启动VNC服务器，并保持进程运行
    vnc_command = "export SHELL=/bin/bash && vncserver :1 -autokill -disableBasicAuth"
    vnc_process = subprocess.Popen(vnc_command, shell=True)

    # 等待一段时间，确保VNC服务器已经启动
    time.sleep(5)

    logger.info("VNC server started. Process ID: %s", vnc_process.pid)

    # # 保持主进程运行，防止VNC服务器被终止
    # try:
    #     while True:
    #         time.sleep(60)  # 每60秒检查一次
    #         if vnc_process.poll() is not None:
    #             logger.error("VNC server process has terminated. Restarting...")
    #             vnc_process = subprocess.Popen(vnc_command, shell=True)
    #             logger.info("VNC server restarted. New Process ID: %s", vnc_process.pid)
    # except KeyboardInterrupt:
    #     logger.info("Received keyboard interrupt. Shutting down VNC server...")
    #     bash("vncserver -kill :1")
    #     vnc_process.terminate()
    #     vnc_process.wait()
    #     logger.info("VNC server shut down.")

    # 端口：8444
