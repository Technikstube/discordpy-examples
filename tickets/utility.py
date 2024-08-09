import json

# tickets.json file
file = "./tickets/tickets.json"

def get_tickets() -> dict:
    with open(file, "r") as f:
        data = json.load(f)
    return data

def save_tickets(tickets: dict) -> None:
    with open(file, "w") as f:
        json.dump(tickets, f, indent=4)