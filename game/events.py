from rich.console import Console
from utils.helpers import load_json
import random

console = Console()

class Events:
    def __init__(self, game_core):
        self.game = game_core
        self.events = load_json("data/events.json")

    def trigger_event(self):
        for event_name, data in self.events.items():
            if random.random() < data["chance"]:
                if data["effect"] == "bonus":
                    self.game.money += data["value"]
                    console.print(f"[green]Событие: '{event_name}' — +${data['value']}[/]", justify="center")
                elif data["effect"] == "penalty":
                    self.game.money -= data["value"]
                    console.print(f"[red]Событие: '{event_name}' — -${data['value']}[/]", justify="center")