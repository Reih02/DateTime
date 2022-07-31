def server(port_1, port_2, port_3):
    port_vars = [port_1, port_2, port_3]
    if len(set(port_vars)) != len(port_vars):
        # not all unique port values
        print("All port numbers must be unique!")
        quit()
    elif not all(x >= 1024 and x <= 64000 for x in port_vars):
        # checks if any port values are less than 1024 or greater than 64000
        print("All port numbers must be between 1024 and 64000!")
        quit()


print(server(1890, 1510, 64001))
