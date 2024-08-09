import json

# tickets.json file
file = "./tickets/tickets.json"

def get_tickets() -> dict:
    """Gets the tickets out of the tickets.json file

    Returns:
        dict: the dict with the ticket data
    """
    with open(file, "r") as f:
        data = json.load(f)
    return data

def save_tickets(tickets: dict) -> None:
    """Saves a dict to the tickets.json

    Args:
        tickets (dict): The dict to save
    """
    with open(file, "w") as f:
        json.dump(tickets, f, indent=4)