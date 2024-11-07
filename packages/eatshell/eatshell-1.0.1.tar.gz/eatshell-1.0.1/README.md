<h1 align="center">eatshell</h1>

<p align="center">
  <a href="#summary">Summary</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
</p>

## Summary

eatshell is a simple command line tool to automate the process of shellcode extraction, loading and assembling. eatshell contains three commands `extract`, `load`, and `assemble`.

**Note: eatshell is meant for small-scale application and primarily created for personal use only.**

## Requirements

- Python 3.xx

## Installation

There are two ways to install `eatshell`:

Install the tool directly with `pip`
```bash
pip install eatshell
```

Or, you can build from source. Download the latest [release](https://github.com/sapphicart/eatshell/releases).

## Usage

Use the `--help` switch to read the `COMMANDS` and `OPTIONS` available.
```bash
$ eatshell --help
Usage: eatshell.py [OPTIONS] COMMAND [ARGS]...

Options:
  --hush  Suppress Usage and Warning info.
  --help  Show this message and exit.

Commands:
  assemble
  extract
  load
```
There are three commands available for `eatshell`:
- assemble
- extract
- load

```bash
$ eatshell assemble --shellcode <hex string> --file <filename>
    
    Use this command to assemble given shellcode
    into an ELF file with +rwx permissions for
    the owner.
```

```bash
$ eatshell extract --file <filename> --hex <boolean>
        
    Use this command to extract shellcode
    from an existing ELF file.
    Turn --hex on for hex encoding.
```

```bash
$ eatshell load --shellcode <hex string>

    Use this command to run the provided
    shellcode interactively.
    Use with caution, might not work everytime.
```

## License
Distributed under [MIT](LICENSE) License.