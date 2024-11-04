# pub-sub-prj
In case you want to test the system on your Linux machine, these are the steps to follow and the terminal commands to use.

1. Download and start the RabbitMQ server on your local machine following the instructions on this [link](https://www.rabbitmq.com/docs/install-debian), choosing the right version of your distribution.

2. Download the necessary libraries and Python 3 to execute correctly the system:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip install matplotlib pika zmq
```

3. Also enable the management plugin and create the cluster of 3 RabbitMQ server instances on the same local machine:
```bash
sudo rabbitmq-plugins enable rabbitmq_management

sudo RABBITMQ_NODE_PORT=5673 RABBITMQ_SERVER_START_ARGS="-rabbitmq_management listener [{port,15673}]" RABBITMQ_NODENAME=rabbit2 rabbitmq-server -detached
sudo RABBITMQ_NODE_PORT=5674 RABBITMQ_SERVER_START_ARGS="-rabbitmq_management listener [{port,15674}]" RABBITMQ_NODENAME=rabbit3 rabbitmq-server -detached

sudo rabbitmqctl -n rabbit2 stop_app
sudo rabbitmqctl -n rabbit2 join_cluster rabbit@<your_hostname>
sudo rabbitmqctl -n rabbit2 start_app

sudo rabbitmqctl -n rabbit3 stop_app
sudo rabbitmqctl -n rabbit3 join_cluster rabbit@<your_hostname>
sudo rabbitmqctl -n rabbit3 start_app
```
obtaining a cluster with rabbit (listening on port 5672 by default), rabbit2 (listening on port 5673) and rabbit3 (listening on port 5674) machines. The first one was already created by the installation mentioned in point 1.

4. Clone this repository:
```bash
git clone <https://github.com/Cristyl/pub-sub-prj.git>
```

5. Move inside the newly cloned repository and then you can start the system with the start.sh file, whose syntax is this:
```bash
./start.sh <rabbitmq|zeromq> <num_of_pubs> <num_of_subs>
```
For instance, you could do this:
```bash
./start.sh rabbitmq 2 5
```
that will start the system in rabbitmq mode and generate 2 publishers and 5 subscribers. If you want to start the system in zeromq mode, you will insert this option instead of rabbitmq, in the example command; the same thing goes for the number of publishers and subscribers.

**Observation.** For a more accurate and a little closer execution to a real distributed system, you should make sure that each started process of this project is handled by at least 1 core of your local machine CPU, simulating that each of them is physically located in a separate node. This could be possible by modifying the processes priorities on that machine, for instance by following this [guide](https://www.redhat.com/sysadmin/manipulate-process-priority).
