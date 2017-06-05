1. IP address: 35.165.43.167 username: ubuntu / grader


2. URL for web application

	http://35.165.43.167/catalog


3. Software Installed and Configuration changes

	- update & upgrade system
	- add port 123 to firewall
	- add port 2200(ssh) to firewall
	- sshd_config: add port 2200; PermitRootLogin = no;
	- remove port 22 in firewall
	- add user grader, password: FSNDgrader
	- add grader file in sudoers.d
	- generate rsa key pair, passPhrase: FSNDgrader
	- copy pub key from local computer to AWS
	- remove port 22 in /etc/ssh/sshd_config
	- Change mod: .ssh 700; .ssh/authorized_keys 600;
	- Installed apache
	- Installed WSGI and configured .wsgi file location
	- Tested myapp.wsgi to print 'hello world!'
	- Installed postgresql
	- Installed python-pip
	- Installed flask
	- installed unzip and unziped previous proj_5 files
	- installed python-sqlalchemy
	- pip installed Flask-Login oauth2client requests
	- installed python-psycopg2
	- installed sqlite3
	- Enabled UFW and set rules

4. Third Parth resources

	[scp with port number specified](https://stackoverflow.com/questions/10341032/scp-with-port-number-specified)
	
	[What is the difference between ssh_config and sshd_config](https://prasadlinuxblog.wordpress.com/2012/09/13/what-is-the-difference-between-ssh_config-and-sshd_config/)
	
	[Secure Your Instance](http://jeffreifman.com/how-to-install-your-own-private-e-mail-server-in-the-amazon-cloud-aws/secure-your-instance/)
	
	[ProgrammingError Thread error in SQLAlchemy](https://stackoverflow.com/questions/15140554/programmingerror-thread-error-in-sqlalchemy)
