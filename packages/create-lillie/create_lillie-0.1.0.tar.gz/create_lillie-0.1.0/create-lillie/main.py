import typer
import os
import shutil
import colorama

def create(name: str = "app"):
    source_dir = "../lilliepy"
    destination_dir = os.path.join(os.getcwd(), name)

    if os.path.exists(destination_dir):
        print(colorama.Fore.RED + f"Directory {destination_dir} already exists...")

    shutil.copytree(source_dir, destination_dir)
    print(colorama.Fore.GREEN + f"{name} has been created!")

if __name__ == '__main__':
    typer.run(create)
