from rich.console import Console
from utils.helpers import load_json

console = Console()

class Staff:
    def __init__(self, game_core):
        self.game = game_core
        self.staff = {"Бариста": {"count": 1, "skill": 1.0, "salary": 100, "morale": 100}}
        self.morale_decay = 5

    def hire(self, role, count, salary, skill):
        if self.game.money >= salary * count:
            self.game.money -= salary * count
            if role in self.staff:
                self.staff[role]["count"] += count
            else:
                self.staff[role] = {"count": count, "skill": skill, "salary": salary, "morale": 100}
            self.game.staff_count += count
            self.update_efficiency()
            console.print(f"[green]Нанято {count} {role} за ${salary * count}.[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для найма![/]", justify="center")

    def fire(self, role, count):
        if role in self.staff and self.staff[role]["count"] >= count:
            self.staff[role]["count"] -= count
            self.game.staff_count -= count
            if self.staff[role]["count"] <= 0:
                del self.staff[role]
            self.update_efficiency()
            console.print(f"[green]Уволено {count} {role}.[/]", justify="center")
        else:
            console.print("[red]Нельзя уволить больше, чем есть![/]", justify="center")

    def daily_salary(self):
        total_salary = sum(s["count"] * s["salary"] for s in self.staff.values())
        if self.game.money >= total_salary:
            self.game.money -= total_salary
            console.print(f"[red]Выплачена зарплата: ${total_salary}[/]", justify="center")
        else:
            self.game.money = 0  # Не уходим в минус
            console.print(f"[red]Недостаточно денег для зарплаты (${total_salary})! Персонал недоволен![/]", justify="center")
            for role in self.staff:
                self.staff[role]["morale"] -= 10  # Дополнительное снижение морали
        for role in self.staff:
            self.staff[role]["morale"] -= self.morale_decay
            if self.staff[role]["morale"] < 0:
                self.staff[role]["morale"] = 0
        self.update_efficiency()
        console.print(f"[yellow]Мораль персонала: {self.get_average_morale()}%[/]", justify="center")

    def update_efficiency(self):
        if self.game.staff_count > 0:
            self.game.staff_efficiency = sum(s["count"] * s["skill"] * (s["morale"] / 100) for s in self.staff.values()) / self.game.staff_count
        else:
            self.game.staff_efficiency = 1.0

    def boost_morale(self, amount):
        cost = amount * 10 * self.game.staff_count
        if self.game.money >= cost:
            self.game.money -= cost
            for role in self.staff:
                self.staff[role]["morale"] = min(100, self.staff[role]["morale"] + amount)
            self.update_efficiency()
            console.print(f"[green]Мораль персонала повышена на {amount}% за ${cost}.[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для повышения морали![/]", justify="center")

    def get_average_morale(self):
        if self.game.staff_count > 0:
            return int(sum(s["morale"] * s["count"] for s in self.staff.values()) / self.game.staff_count)
        return 100

    def load_staff(self):
        return load_json("data/staff.json")