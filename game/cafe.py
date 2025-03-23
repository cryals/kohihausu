from rich.console import Console
from data.config import LOCATIONS

console = Console()

class Cafe:
    def __init__(self, game_core):
        self.game = game_core
        self.location = "Центр города"
        self.daily_cost_value = 200
        self.client_bonus = LOCATIONS[self.location]["clients_bonus"]

    def change_location(self, new_location, cost):
        if self.game.money >= cost:
            self.game.money -= cost
            self.location = new_location
            self.client_bonus = LOCATIONS[new_location]["clients_bonus"]
            self.game.clients += self.client_bonus
            console.print(f"[green]Локация изменена на '{new_location}' за ${cost}. Клиенты: +{self.client_bonus}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для смены локации![/]", justify="center")

    def daily_cost(self):
        if self.game.money >= self.daily_cost_value:
            self.game.money -= self.daily_cost_value
            console.print(f"[red]Ежедневные расходы на содержание: ${self.daily_cost_value}[/]", justify="center")
        else:
            self.game.money = 0  # Не уходим в минус
            console.print(f"[red]Недостаточно денег для ежедневных расходов (${self.daily_cost_value})![/]", justify="center")