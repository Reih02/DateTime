def server(port_1, port_2, port_3):
    vars = [port_1, port_2, port_3]
    if len(set(vars)) != len(vars):
        # not all unique values
        print("All port numbers must be unique!")
        quit()
    elif not all(x >= 1024 and x <= 64000 for x in vars):
        print("All port numbers must be between 1024 and 64000!")
        quit()


print(server(1890, 1510, 64001))
