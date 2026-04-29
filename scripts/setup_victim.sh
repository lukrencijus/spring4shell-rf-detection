#!/usr/bin/env bash
set -e

response=""

echo "This script installs required dependencies (docker, tshark, python3-requests) and(or) launches the victim container."

read -p 'Do you want to install dependencies (first time run) y/n?' response

if [ "$response" == "y" ] ; then
	# Docker installation

	# Add Docker's official GPG key:
	apt update
	apt install ca-certificates curl -y
	install -m 0755 -d /etc/apt/keyrings
	curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
	chmod a+r /etc/apt/keyrings/docker.asc

	# Add the repository to Apt sources:
	tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

	apt update

	apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
	apt install python3 -y
	apt install python3-requests -y

	# Tshark installation (allow non-root capture)
	echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
	DEBIAN_FRONTEND=noninteractive apt install tshark -y
	usermod -aG wireshark $SUDO_USER 2>/dev/null || usermod -aG wireshark $USER
	echo "Note: Log out and back in for wireshark group to take effect"

elif [ "$response" != "n" ] ; then
	echo "Invalid input detected"
	echo "Exiting..."
	exit 0
fi
	cd ../victim
	docker build . -t spring4shell
	docker run -d -p 8080:8080 spring4shell
