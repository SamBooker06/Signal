# Signal Networking Library

**Signal is designed for event based networking in python.**

## Creating Server and Client

Create server through `Server(ip, port)`, and run with `.run()`. When a client connects, the server will represent their connection with The `Connection` object

Create clients with `Client(ip, port)`, and connect with `.connect()`

---

## Connecting to Events

Both the server, client and connection have many events to help with networking

### Server

#### Handle a New Connection

```
@server.OnConnection
def handle_connection(conn):
	print("A client has connected!")
```

### Client

#### Handle Connection Complete

```
@client.OnConnection
def handle_connection():
	print("Connected to the server!")

```
