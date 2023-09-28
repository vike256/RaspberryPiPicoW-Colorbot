def move(x, y, client):
    # Mouse.Move takes char (8 bits) as input
    # 8bit signed value range is from -128 to 127
    max = 127
    if abs(x) > abs(max):
        x = x/abs(x) * abs(max)
    if abs(y) > abs(max):
        y = y/abs(y) * abs(max)

    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = f"M{x},{y}\r"
    client.sendall(command.encode())
    print(f"SENT: Move({x}, {y})")
    waitForResponse(client)


def click():
    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = "C\r"
    client.sendall(command.encode())
    print("SENT:Click")
    waitForResponse()


def waitForResponse(client):
    ack = client.recv(4).decode()
    if ack == "ACK\r":
            print("ack received")