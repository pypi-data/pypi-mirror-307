from pwn import *
import os, stat
import click
from colorama import Fore
from dotenv import load_dotenv

load_dotenv()

def shellcoder(filename, hex):
    try:
        file = ELF(filename)
    except FileNotFoundError as e:
        print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
        exit()
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
        exit()

    if hex:
        try:
            shellcode = file.section(".text")
            if hex:
                print(f"{Fore.LIGHTGREEN_EX}\n[+] Success! Here's your code:")
                print(f"{Fore.MAGENTA}{shellcode.hex()}\n")
            else:
                print(f"{Fore.MAGENTA}{shellcode}")
            #print("%d bytes - Found NULL byte" % len(shellcode)) if [i for i in shellcode if i == 0] else print("%d bytes - No NULL bytes" % len(shellcode))
            print(f"{Fore.LIGHTBLUE_EX}Shellcode length: {len(shellcode)} bytes")
            if 0 in shellcode:
                print(f"{Fore.LIGHTRED_EX}[!!] Warning: Found NULL byte")
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+] No NULL bytes!")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode.")



def loader(shellcode):
    if shellcode:
        try:
            run_shellcode(unhex(shellcode)).interactive()
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode. Please provide a valid hex string.")



def assembler(shellcode, filename):
    if shellcode and filename:
        try:
            ELF.from_bytes(unhex(shellcode)).save(filename)
            os.chmod(filename, stat.S_IREAD|stat.S_IWRITE|stat.S_IEXEC)
            print(f"{Fore.LIGHTGREEN_EX}[+] Success: Code successfully assembled to {Fore.CYAN}./{filename}")
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
    elif not shellcode:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode. Please provide a valid hex string.")
    elif not filename:
        print(f"{Fore.RED}[-] Error: Could not create file. Please provide a valid filename.")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse shellcode or filename. Please provide a valid hex string and filename to write.")


@click.group()
@click.option('--hush', is_flag=True, help="Suppress Usage and Warning info.")
def cli(hush):
    system = os.getenv('OS')
    arch = os.getenv('ARCH')
    log_level = os.getenv('LOG_LEVEL')
    #context(os="linux", arch="amd64", log_level="error")\

    if system and arch and log_level:
        try:
            context(os=system, arch=arch, log_level=log_level)
        except Exception as e:
            print(f"{Fore.RED}[-] Error: {Fore.LIGHTRED_EX}{e}")
    else:
        print(f"{Fore.RED}[-] Error: Could not parse context. Create a .env file with the required parameters. Check Usage for more details.")


    print(f"""{Fore.YELLOW}
        ⠀⠀⠀⠀⣀⣤⣴⣶⣶⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⢿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀            
        ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣅⢀⣽⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠁⠀⠀⣴⣶⡄⠀⣶⣶⡄⠀⣴⣶⡄
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⠀⠙⠋⠁⠀⠉⠋⠁⠀⠙⠋⠀
        ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀         
        ⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠈⠙⠿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
             _       _          _ _  
            | |     | |        | | | 
   ___  __ _| |_ ___| |__   ___| | | 
  / _ \/ _` | __/ __| '_ \ / _ \ | | 
 |  __/ (_| | |_\__ \ | | |  __/ | | 
  \___|\__,_|\__|___/_| |_|\___|_|_| 
    """)
    if not hush:
        print(f"""{Fore.LIGHTMAGENTA_EX}
Creator: sapphicart
    {Fore.YELLOW}
Usage: eatshell [COMMAND] options [ARGUMENTS]

Commands:
            
    extract
        --file <filename> --hex <boolean>
        Use this command to extract shellcode
        from an existing ELF file.
        Turn --hex on for hex encoding.
            
    load
        --shellcode <hex string>
        Use this command to run the provided 
        shellcode interactively. 
        Use with caution, might not work everytime.
            
    assemble
        --shellcode <hex string> --file <filename>
        Use this command to assemble given shellcode 
        into an ELF file with +rwx permissions for 
        the owner.
            
{Fore.LIGHTRED_EX}[!!] IMPORTANT [!!]

Context Vars: Create an .env file with the following
variables. Otherwise, the program might not work.

    .env file structure example:

        OS=linux
        ARCH=amd64
        LOG_LEVEL=error

{Fore.CYAN}Suppress Usage and Warning info with --hush
switch.{Fore.RESET}
        """)

    else:
        print(f"{Fore.YELLOW}[/] Usage and Warning info suppressed.\n{Fore.RESET}")


@click.command()
@click.option('--file', help="Enter the filename to extract shellcode.")
@click.option('--hex', help="Turn hex mode on/off with --hex True/False.", is_flag=True)
def extract(file, hex):
    print(f"{Fore.LIGHTYELLOW_EX}[\] Running extract command...\n")
    shellcoder(file, hex)


@click.command()
@click.option('--shellcode', type=str, help="Enter the shellcode as a hex string.")
def load(shellcode):
    print(f"{Fore.LIGHTYELLOW_EX}[\] Running load command...\n")
    loader(shellcode)


@click.command()
@click.option('--shellcode', help="Enter the shellcode as a hex string.")
@click.option('--file', help="Enter the output filename.")
def assemble(shellcode, file):
    print(f"{Fore.LIGHTYELLOW_EX}[\] Running assemble command...\n")
    assembler(shellcode, file)


cli.add_command(extract)
cli.add_command(load)
cli.add_command(assemble)


if __name__=='__main__':
    cli()