# tango-little-rest

Simple REST server to read device info, commands and attributes.

When tango-test device server is running then we can use these links:
localhost:5000/devices/sys/tg_test/1
localhost:5000/devices/sys/tg_test/1/attributes/ampli
localhost:5000/devices/sys/tg_test/1/commands/last
localhost:5000/devices/sys/tg_test/1/commands/10

It was tested using Jive and changing values of device attributes and info of a few other devices.
