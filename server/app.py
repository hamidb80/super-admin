from server import tunnel
from events import event_list


# register events
for event in event_list:
    tunnel.on(event.name, event.function)

if __name__ == "__main__":
    tunnel.run()
