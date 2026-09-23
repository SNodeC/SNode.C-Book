# Persistence and Full Systems

Part VIII widened the communication picture from one stack to several cooperating roles. This part adds the state that survives individual exchanges and then studies complete executable systems.

MariaDB-backed persistence leads to reading complete applications in `src/apps`, then to a separate chapter on system composition and MQTTSuite. This order distinguishes an executable’s assembly from responsibilities shared across processes. Part X then turns to the build, installation, and maintenance surfaces that make those systems reproducible.

The checkpoint reads a committed measurement after the database client restarts, then contrasts the gateway’s transient state. Use those observations to separate broker delivery, raw storage and projection when tracing a publication through the worked system.
