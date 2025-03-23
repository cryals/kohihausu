from rich.console import Console

console = Console()

class Themes:
    def __init__(self):
        self.themes = {
            "Лесной мотив": {"border": "green", "text": "cyan"},
            "Кофейный нуар": {"border": "white", "text": "grey"},
            "Зверополис": {"border": "magenta", "text": "yellow"}
        }
        self.current_theme = "Зверополис"

    def set_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = theme_name
            console.print(f"[green]Тема изменена на '{theme_name}'.[/]", justify="center")
        else:
            console.print("[red]Такой темы нет![/]", justify="center")

    def get_style(self, element):
        return self.themes[self.current_theme].get(element, "")