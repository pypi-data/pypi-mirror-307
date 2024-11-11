import httpx as hx
import os
import tqdm as td

from . import constants as cs

cwd = os.getcwd()

def download(link: str, path: str, progress = True, description = None) -> None:
    """Download data from 'link' and store at 'path'."""
    
    if description is not None:
        print(f"Downloading {description}...")
    
    with hx.Client(http2 = True) as client:
        with client.stream("get", link) as response:
            with open(path, "wb") as file:
                total = int(response.headers.get("Content-Length", 0))
                with td.tqdm(total = total, \
                             unit_scale = True, \
                             unit_divisor = 2**10, \
                             unit = "B", \
                             disable = not progress) as progress:
                    num_bytes_downloaded = response.num_bytes_downloaded
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                        progress.update(response.num_bytes_downloaded)
                        num_bytes_downloaded = response.num_bytes_downloaded

def question(string: str) -> bool:
    """Ask the user a Y/N question and return the accompagnied truth value."""
    while True:
        choice = input(f"{string} (Y/N): ").lower()
        
        if choice in cs.answers_true:
            return True
        elif choice in cs.answers_false:
            return False
        else:
            print("This is not an option. Please try again.")

def drive_selection() -> str:
    """Select a drive for a directory."""
    
    # Select drive for Windows only
    if os.name == "nt":
        # Collect available drives
        drives = []
        for letter in [chr(x) for x in range(ord("A"), ord("A") + 26)]:
            if os.path.exists(f"{letter}:"):
                drives.append(letter)
        
        # Print all drives
        for letter in drives:
            print(f"{letter}. Drive {letter}:")
        
        # Select a drive
        while True:
            drive = input("Which drive should be selected? (Enter the corresponding option): ").upper()
            
            if drive in drives:
                return f"{drive}:"
            else:
                print("This is not an option. Please try again.")
    else:
        return os.path.splitdrive(cwd)[0]

def clear_screen() -> None:
    """Clear the screen for Windows and Unix-based systems."""
    
    os.system("cls" if os.name == "nt" else "clear")
