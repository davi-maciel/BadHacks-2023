import typer
from rich import print
from rich.panel import Panel
import save
app = typer.Typer()


data = save.load()


@app.command()
def hello(name=data.get('name', '')):
    data['name'] = name
    
    print(Panel(f"[magenta]Hello {name}![/magenta]", title="CLI Girfriend"))
    save.save(data)
    

@app.command()
def goodbye(name=data.get('name', ''), formal: bool = False):
    if formal:
        print(f"Goodbye Mr. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

@app.command()
def reset():
    save.save({})


if __name__ == "__main__":
    app()