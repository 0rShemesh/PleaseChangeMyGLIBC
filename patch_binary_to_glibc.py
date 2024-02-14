import lief
from os import getenv
from pathlib import Path
import subprocess
import typer

GLIBC_TAG =  getenv("GLIBC_TAG","glibc-2.39")
GLIBC_PATH = Path("builds") / GLIBC_TAG / "elf"


class ELFInjector:
    binary: lief.Binary
    def  __init__(self, elf_manipulate:Path):
        self.binary = lief.parse(str(elf_manipulate))

    
    def inject_library_path(self,library_path:Path):
        library_path_entry = lief.ELF.DynamicEntryRpath(str(library_path))
        self.binary.add(library_path_entry)
    
    def remove_library(self, library_name):
        self.binary.remove_library(library_name)

    def inject_library(self, library:str, library_path:str = None):
        if not library_path:
            library_path = str(Path(library_path).absolute().parent)
        
        self.binary.add_library(library)

    def add_hook(self, hook_name,hook_symbol, hook_file_source):
        subprocess.run(["gcc","-Os","-nostdlib","-nodefaultlibs","-fPIC","-Wl,-shared",hook_file_source,"-o", f"{hook_name}.so"])
        hook_elf = lief.parse(f"{hook_name}.so")
        
        symbol_to_hook = self.binary.get_symbol(hook_symbol)
        symbol_that_hook = hook_elf.get_symbol(hook_name)
        code_segment  = hook_elf.segment_from_virtual_address(symbol_that_hook.value)
        segment_added  = self.binary.add(code_segment)
        new_address = segment_added.virtual_address + symbol_that_hook.value - code_segment.virtual_address
        symbol_to_hook.value = new_address
        symbol_to_hook.type = lief.ELF.Symbol.TYPE.FUNC


    def write(self, new_name:Path):
        self.binary.write(str(new_name))




def main(filename:Path, libc_location_path:Path = GLIBC_PATH) -> None:
    elf = ELFInjector(str(filename))
    elf.inject_library_path(libc_location_path)
    elf.write(filename.parent / f"patched_{filename.name}")


if __name__ == "__main__":
    typer.run(main)

