1. IP address: 35.165.43.167 username: ubuntu


2. URL for web application


3. Software Installed and Configuration changes

	- update & upgrade
	- add port 123 to firewall
	- add port 2200(ssh) to firewall
	- sshd_config: add port 2200; PermitRootLogin no;
	- remove port 22 in firewall
	- add user grader, password: FSNDgrader
	- add grader file in sudoers.d
	- generate rsa key pair, passPhrase: FSNDgrader
	- copy pub key to ~/.ssh/authorized_keys
	- remove port 22 in /etc/ssh/sshd_config
	- .ssh 700; .ssh/authorized_keys 600;

4. Third Parth resources
