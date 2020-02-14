from time import sleep

i = 0

while i != 10:
    print(i + 1)
    i += 1
    sleep(0.2)

    if i is 8:
        raise EOFError
