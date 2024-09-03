install:
	python3 -m venv venv

run_virtual_enviroment:
	source venv/bin/activate

install_node_modules:
	npm install

run_server:
	node webserver.js

