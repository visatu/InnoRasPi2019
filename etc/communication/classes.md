#Classes for RasPi communications module
-abstract classes for station and actuator/sensor, to be used in main. Includes all relevant info on the station: Name, encoded name, address, connected actuators/sensors objects.
    -RasPi dev
    -XBee dev
    -other?

-Abstract dev:
    -name
    -dev type
    -sensors list
-Abstract sensor
    -name
    -sensor type
    -value

-master class for single actuator/sensor
-Message class for communication between main and communications module:
    -Msg type
    -timestamp
    -name
    -msg id
        subclasses:
        -Value
            -Value
            -request
        -Dev change
            -new
            -device
            -sensors
