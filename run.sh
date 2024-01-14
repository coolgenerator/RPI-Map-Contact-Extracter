#!/bin/bash

# Script to initialize basic environment and run the code
# @Author: Jason Wang <jiw196@ucsd.edu>
# @Version: 0.1.0
#      ____                  __  ___  __             
#      / /__  ___ ___  _____ || /  | / /__  ________ 
#  __ / / _ `(_-</ _ \/ _  / ||/ /||/ / _ `/ _  / _ `
#  \___/\_,_/___/\___/_//_/  |__/ |__/\_,_/_//_/\_, /
#                                              /___/ 


MCE_DB_NAME="MapContactExtracter"
MCE_DB_USER="MapContactUser"
MCE_DB_PASS='3xtr@ctC0nt@ct$2024!'
SQL_SCRIPT="create_tables.sql"

# Install mariadb base on operating system
install_mariadb() {
	unameOut="$(uname -s)"

	case $unameOut in
		Linux*)
			echo "Installing Mariadb for Linux ..."
			# Install Mariadb for Debian/Unbuntu systems
			if [ -f /etc/debian_version ]; then
				echo "Debian/Ubuntu system Detected"
				sudo apt-get update
				sudo apt-get install mariadb-server -y

			# Install Mariadb for Red Hat/CentOS systems
			elif [ -f /etc/fedora-release ]; then
				echo "Fedora system Detected"
				sudo dnf update
				sudo dnf install mariadb-server -y

			# Install Mariadb for Red Hat/CentOS systems
			elif [ -f /etc/redhat-release ]; then
				echo "Red Hat/CentOS system Detected"
				sudo yum update
				sudo yum install mariadb-server -y
			else
				echo "Unsupported Linux system."
			fi
			;;
		Darwin*)
			echo "Installing Mariadb for Mac ..."
			# check if Homebrew is installed
			if ! command -v brew &>/dev/null; then
				echo "Homebrew not found. Installing Homebrew."
				/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
			fi
			# Install MariaDB using Homebrew
			brew update
			brew install mariadb
			;;
		*)
			echo "Unsupported operating system."
			;;
	esac

}

initialize_database() {
	# login database
	if mysql -u"$DB_USER" -p"$DB_PASS" -e "quit" 2>/dev/null; then
        echo "Successfully connected to MySQL"
    else
        echo "Setup MCE user"
		sudo mysql -e "SET PASSWORD FOR $MCE_DB_USER@'localhost' = PASSWORD($MCE_DB_PASS); FLUSH PRIVILEGES;"
    fi
}

main() {
	echo "Checking for MariaDB installation..."
	# Check database status, install if not exist
	if command -v mysql &>/dev/null && mysql --version | grep -qi 'MariaDB'; then
		initialize_database
	else
		echo "Mariadb is not installed"
		install_mariadb
		initialize_database
	fi

	# Run SQL script to create required tables
	mysql -u"$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS $MCE_DB_NAME;"
	mysql -u"$DB_USER" -p"$DB_PASS" -D "$MCE_DB_NAME" < "$SQL_SCRIPT"
}

main "$@"
