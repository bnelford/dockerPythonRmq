This is a project that allows the scale testing of a local rabbitMQ docker instance with publishers.

Requirements:
Docker engine 1.8+ (because of the python containers)
Docker-compose binary 1.5.2+

How to use:

Set your local IP address in the basic reader and basic writer files.
(replace "@localmachineIPaddr@" with your IP address)

docker-compose up -d

This brings up 1 rabbitMQ instance, one basic python rabbitmq reader, and one pubisher.

To change the scale -

-Scale the readers to 10 containers
docker-compose scale reader=10

-Scale the readers to 10 containers
docker-compose scale publisher=10

A few notes:
The reader's prefetch is set to 0 - I did this so that no messages would be lost upon reader exit.
The python is a but sloppy, but should be fine.
