# erebor
Erebor is a lightweight key-value store with a Redis-like syntax.

## Installation
To install the erebor server:
```bash
pip install erebor
```

## Usage
Run the server like so:
```bash
$ erebor
```

You can verify erebor is running by connecting to 127.0.0.1:8044.
```bash
$ nc localhost 8044
keys
[]
set foo bar
OK
keys
["foo"]
get foo
bar
```

## API
Erebor recognizes the following commands:
```
    set   <key> <value>  set a key to a value
    del   <key>          remove a key and its value
    get   <key>          retrieve the value of a key
    keys  [prefix]       return a list of keys starting with prefix
```

## Configuration
By default, erebor listens on 127.0.0.1:8044. You can change this as follows:

```bash
$ erebor -b 0.0.0.0 -p 8055
```

For security reasons, it is not recommended to bind on 0.0.0.0 and expose the
database to the world.

By default, erebor runs in ephemeral mode, where keys are only stored in memory.
To run in durable mode, simply specify the `-d` option:

```bash
$ erebor -d /path/to/database
```

This will save the database to disk at the specified path.

## Other notes
The erebor API uses vanilla TCP sockets, so you can make API requests using `netcat`.
```bash
$ echo "set home $(cat index.html)" | nc -q 0 localhost 8044
OK
```

You can also talk to erebor programmatically using any language that can speak TCP:
```python
import socket

# Setup a socket to the host and port where erebor is running.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 8044))

def erebor(message):
    sock.send(message.encode())
    return sock.recv(1024).decode().strip()

print(erebor("set foo bar"))
# OK
print(erebor("get foo"))
# bar
```
