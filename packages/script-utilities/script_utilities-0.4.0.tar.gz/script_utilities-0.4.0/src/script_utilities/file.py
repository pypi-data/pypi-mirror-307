import os
import pickle as pk
import shutil as sh
import typing as tp

cwd = os.getcwd()

class File(object):
    
    def __init__(self, path: str) -> None:
        basepath, extension = os.path.splitext(path)
        
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(basepath)
        self.extension = extension
    
    def __repr__(self) -> str:
        """Returns the path of the file."""
        
        return self.path
    
    def __bool__(self) -> bool:
        """Returns true or false based on if the file exists or not."""
        
        return os.path.exists(self.path)
    
    def rename(self, filename: str) -> None:
        """Renames a file."""
        
        new_path = os.path.join(self.folder, filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move(self, path: str) -> None:
        """Moves a file to a new path. The filename must stay the same."""
        
        if self.filename + self.extension != os.path.basename(path):
            raise ValueError("filename does not match")
        
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        sh.move(self.path, path)
        self.__init__(path)
    
    def move_down(self, folders: list[str], create = True) -> None:
        """Moves a file down into the folders listed in order."""
        
        if not isinstance(folders, list):
            raise TypeError("unsupported operand type(s) for move_down: "
                            f"'{type(self).__name__}' and '{type(folders).__name__}'")
        
        new_folder = self.folder
        for folder in folders:
            new_folder = os.path.join(new_folder, folder)
        
        if not os.path.exists(new_folder):
            if not create:
                raise FileNotFoundError("directory created by 'folders' does not exist")
            else:
                os.makedirs(new_folder)
        
        new_path = os.path.join(new_folder, self.filename + self.extension)
        sh.move(self.path, new_path)
        self.__init__(new_path)
    
    def move_up(self, amount: int) -> None:
        """Moves a file up an arbitrary amount of folders."""
        
        if not isinstance(amount, int):
            raise TypeError("unsupported operand type(s) for move_up: "
                            f"'{type(self).__name__}' and '{type(amount).__name__}'")
        
        for x in range(amount):
            self.move(os.path.join(os.path.dirname(self.folder), self.filename + self.extension))
        
    def copy(self, path: str) -> tp.Self:
        """Copies a file to a new path."""
        
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        sh.copyfile(self.path, path)
        return File(path)
    
    def delete(self) -> None:
        """Deletes a file."""
        
        os.remove(self.path)

class Folder(File):
    
    def copy(self, path: str) -> tp.Self:
        """Copies a folder to a new path."""
        
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        sh.copytree(self.path, path)
    
    def merge(self, other: tp.Self) -> None:
        """Merges two folders into one."""
        
        if not isinstance(other, Folder):
            raise TypeError("unsupported operand type(s) for merge: "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        if self.path == other.path:
            return
        
        for file in os.listdir(other.path):
            if os.path.isfile(os.path.join(other.path, file)):
                old = File(os.path.join(self.path, file))
                new = File(os.path.join(other.path, file))
            else:
                old = Folder(os.path.join(self.path, file))
                new = Folder(os.path.join(self.path, file))
            
            if isinstance(old, File):
                if bool(old) and bool(new):
                     old.delete()
                new.move(old.path)
            else:
                old.merge(new)
        
        other.delete()
    
    def delete(self) -> None:
        """Deletes a folder."""
        
        sh.rmtree(self.path)

class TXT(File):
    
    def read(self) -> list[str]:
        """Returns the contents of a text file as a list of strings."""
        
        with open(self.path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
        
        return lines
    
    def write(self, lines: list[str]) -> None:
        """Writes a list of strings to a text file."""
        
        with open(self.path, "w", encoding = "utf-8") as file:
            file.writelines("".join(lines))
    
    def rewrite(self, index: int, line: str) -> None:
        """Rewrites a single line from a text file."""
        
        lines = self.read()
        lines[index] = line
        self.write(lines)
    
    def find(self, string: str) -> int:
        """Finds the index of the line that starts with a given string."""
        
        lines = self.read()
        for x, line in enumerate(lines):
            if line.strip().startswith(string):
                return x
    
    def append(self, line: str) -> None:
        """Appends a line to the end of a text file."""
        
        with open(self.path, "a", encoding = "utf-8") as file:
            file.writeline(line)

class PKL(File):
    
    def __init__(self, path: str) -> None:
        if not path.endswith(".pkl"):
            raise ValueError("not a pkl file")
        
        basepath, extension = os.path.splitext(path)
        
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(basepath)
        self.extension = extension
        
        if not bool(self):
            with open(self.path, "wb") as file:
                pk.dump(None, file)
        
    def __repr__(self) -> str:
        """Returns the filename and the value that it contains."""
        
        return f"{self.filename}: {self.get_value()}"
    
    def __str__(self) -> str:
        return repr(self)
    
    def get_value(self):
        """Obtains the current value from the file."""
        
        if not bool(self):
            return
        
        with open(self.path, "rb") as value:
            return pk.load(value)
    
    def set_value(self, value) -> None:
        """Writes any value into the file."""
        
        with open(self.path, "wb") as file:
            pk.dump(value, file)
    
    def pairs(self) -> tuple[str]:
        """Returns the filename and the value that it contains in a tuple."""
        
        return self.filename, self.get_value()

class TXZ(File):
    
    def __init__(self, path: str) -> None:
        if not path.endswith(".txz"):
            raise ValueError("not a txz file")
        
        basepath, extension = os.path.splitext(path)
        
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(basepath)
        self.extension = extension
        self.tar = None
    
    def extract(self) -> None:
        """Extracts a TAR file from the archive."""
        
        old_files = os.listdir(self.folder)
        os.system(f"7z x -o\"{self.folder}\" \"{self.path}\"")
        new_files = os.listdir(self.folder)
        
        for file in new_files:
            if file not in old_files:
                self.tar = TAR(os.path.join(self.folder, file))
                return
    
    def delete(self) -> None:
        """Deletes the file and the extracted TAR file."""
        
        os.remove(self.path)
        if bool(self.tar):
            self.tar.delete()

class TAR(File):
    
    def __init__(self, path: str) -> None:
        if not path.endswith(".tar"):
            raise ValueError("not a tar file")
        
        basepath, extension = os.path.splitext(path)
        
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(basepath)
        self.extension = extension
        self.extracted_folder = None
    
    def extract(self) -> None:
        """Extracts a folder from the archive."""
        
        old_files = os.listdir(self.folder)
        os.system(f"7z x -o\"{self.folder}\" \"{self.path}\"")
        new_files = os.listdir(self.folder)
        
        for file in new_files:
            if file not in old_files:
                self.extracted_folder = Folder(os.path.join(self.folder, file))
                return
    
    def build(self) -> None:
        """Reconstructs the file from the extracted folder."""
        
        if not bool(self.extracted_folder):
            raise FileNotFoundError("tar has never been extracted")
        
        os.remove(self.path)
        os.system(f"7z a \"{self.path}\" \"{self.extracted_folder.path}\"")
        self.extracted_folder.delete()
    
    def delete(self) -> None:
        """Deletes the file and the extracted folder."""
        
        os.remove(self.path)
        if bool(self.extracted_folder):
            self.extracted_folder.delete()
