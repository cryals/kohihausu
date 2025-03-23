from rich.console import Console
from utils.helpers import load_json

console = Console()

class Upgrades:
    def __init__(self, game_core):
        self.game = game_core

    def buy_upgrade(self, name, cost, bonus_type, bonus_value):
        if self.game.money >= cost:
            self.game.money -= cost
            if bonus_type == "comfort":
                self.game.comfort += bonus_value
            elif bonus_type == "reputation":
                self.game.reputation += bonus_value
            elif bonus_type == "efficiency":
                self.game.staff_efficiency += bonus_value
            elif bonus_type == "clients":
                self.game.clients += bonus_value
            console.print(f"[green]Куплено '{name}' за ${cost}. {bonus_type} +{bonus_value}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для покупки![/]", justify="center")

    def load_items(self):
        return load_json("data/items.json")

    def load_marketing(self):
        return load_json("data/marketing.json")