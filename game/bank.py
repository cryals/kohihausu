from rich.console import Console

console = Console()

class Bank:
    def __init__(self, game_core):
        self.game = game_core
        self.loan = 0
        self.deposit = 0
        self.loan_interest = 0.05
        self.deposit_interest = 0.02

    def take_loan(self, amount):
        if self.game.money >= 0:  # Кредит только при положительном балансе
            self.loan += amount
            self.game.money += amount
            console.print(f"[green]Взят кредит ${amount}. Общий долг: ${self.loan}[/]", justify="center")
        else:
            console.print("[red]Нельзя взять кредит при нулевом балансе![/]", justify="center")

    def repay_loan(self, amount):
        if self.game.money >= amount and self.loan >= amount:
            self.game.money -= amount
            self.loan -= amount
            console.print(f"[green]Погашено ${amount}. Остаток долга: ${self.loan}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег или суммы для погашения![/]", justify="center")

    def make_deposit(self, amount):
        if self.game.money >= amount:
            self.game.money -= amount
            self.deposit += amount
            console.print(f"[green]Сделан депозит ${amount}. Общий депозит: ${self.deposit}[/]", justify="center")
        else:
            console.print("[red]Недостаточно денег для депозита![/]", justify="center")

    def withdraw_deposit(self):
        if self.deposit > 0:
            self.game.money += self.deposit
            console.print(f"[green]Снято ${self.deposit} с депозита.[/]", justify="center")
            self.deposit = 0
        else:
            console.print("[red]Депозит пуст![/]", justify="center")

    def daily_update(self):
        if self.loan > 0:
            interest = int(self.loan * self.loan_interest)
            if self.game.money >= interest:
                self.game.money -= interest
                console.print(f"[red]Выплачены проценты по кредиту: ${interest}[/]", justify="center")
            else:
                self.game.money = 0  # Не уходим в минус
                console.print(f"[red]Недостаточно денег для процентов по кредиту (${interest})![/]", justify="center")
        if self.deposit > 0:
            interest = int(self.deposit * self.deposit_interest)
            self.deposit += interest
            console.print(f"[green]Начислены проценты по депозиту: ${interest}[/]", justify="center")