# python-rabbitmq-example
Example for python 3.6+<br>
Installing RabbitMQ with docker:
```
docker run -d --hostname rabbit-host --name rabbit-example -p 15675:15672 -p 127.0.0.1:5675:5672 rabbitmq:3-management
```
On local host **15675** port will be used for GUI and **5675** for RabbitMQ server