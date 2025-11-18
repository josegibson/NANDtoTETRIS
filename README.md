# Nand2Tetris Compiler Suite

*A complete Jack → VM → Assembly → Hack toolchain, built from scratch.*

---

## Overview

This repository contains a fully implemented, modular compiler toolchain for the **Jack programming language**. This project reproduces the entire **software pipeline** from a high-level, object-oriented language down to executable machine code for the Hack computer.

This project was built to showcase:

*   Clean, modular architecture
*   Multi-stage compilation
*   Real compiler techniques (tokenization, recursive descent parsing, symbol tables, and code generation)

---

## Demo

![alt text](demo.gif)

---

## Project Structure

```
/Assembler/      # Translates .asm -> .hack machine code
/VMTranslator/ # Translates .vm -> .asm assembly language
/Compiler/       # Translates .jack -> .vm virtual machine code
/examples/       # Example programs for the toolchain
```

---

## Usage

This repository includes a master script, `main.py`, that automates the entire compilation pipeline. This is the recommended way to compile your Jack projects.

### Automated Pipeline

The `main.py` script in the root directory handles the full Jack → VM → Assembly → Hack compilation process in a single step.

**1. Clone the repo**

```bash
git clone <repo_url>
cd NANDtoTETRIS
```

**2. Run the pipeline**

Use `python main.py` and point it at a Jack file or a directory of Jack files.

```bash
# From D:/NANDtoTETRIS/
# Compile an entire project (e.g., examples/Counter)
python main.py examples/Counter --output examples/Counter
```

This will generate all intermediate files (`.vm`, `.asm`) and the final `.hack` machine code in the specified output directory.

### Manual Compilation (Alternative)

If you want to run each stage of the pipeline manually, follow these steps.

**1. Clone the repo**

```bash
git clone <repo_url>
cd NANDtoTETRIS
```

**2. Compile a Jack program (Jack → VM)**

Navigate to the `Compiler` directory and run the analyzer on a source file or directory.

```bash
# From D:/NANDtoTETRIS/
cd Compiler/
python JackAnalyzer.py ../examples/SimpleAdd/ --output ../examples/SimpleAdd/
```

**3. Translate VM → Assembly**

Navigate to the `VMTranslator` directory to run the translator.

```bash
# From D:/NANDtoTETRIS/
cd VMTranslator/
python main.py ../examples/SimpleAdd/
```

**4. Assemble to Hack machine code**

Navigate to the `Assembler` directory to run the final assembly step.

```bash
# From D:/NANDtoTETRIS/
cd Assembler/
python main.py ../examples/SimpleAdd/Main.asm
```

**5. Run on the Nand2Tetris CPU Emulator**

Load the generated `Main.hack` file into the official CPU emulator to see the result.

### Running VM Code with OS Emulation

For VM code that interacts with the operating system, it is recommended to run the generated `.vm` files directly on the official Nand2Tetris VM Emulator. This emulator provides the necessary OS emulation capabilities.

### Jack Compiler Details

The main entry point for the compiler is the `JackAnalyzer.py` script.

**Prerequisites**

*   Python 3.x

**Execution**

Navigate to the `Compiler/` directory and run the analyzer from your terminal.

```bash
# Navigate to the Compiler directory
cd Compiler/

# Run the analyzer on a source file or directory
python JackAnalyzer.py <path/to/source.jack_or_directory>
```

**Command-Line Arguments**

The analyzer accepts several optional flags to control its behavior:

*   `--output <directory>`: Specify a directory to write the output `.vm` files to. If omitted, the output is not saved.
*   `-m, --mode [vm|xml]`: Choose the output mode. Defaults to `vm` for code generation. Use `xml` to generate a parse tree for debugging.
*   `-v, -vv, -vvv`: Increase the output verbosity for debugging.
    *   `-v`: Prints class-level scope information.
    *   `-vv`: Also prints subroutine-level scope information.
    *   `-vvv`: Also prints the generated VM code for each subroutine.

**Example:**

```bash
# Compile an entire project and see full debug output
python JackAnalyzer.py ../examples/Counter/ -vvv --output ../compiled_output/
```

---

## Architecture

This project was built with a focus on clean architecture and modular, single-responsibility design patterns.

### 1. Two-Pass Architecture

Both the Assembler and the Jack Compiler use a **two-pass architecture** to handle forward references (e.g., using a variable or calling a function before it is declared).

*   **First Pass (Symbol Table Construction):** The compiler scans the source code to build a complete **Symbol Table**, mapping every identifier (variable, label, subroutine) to its properties (type, kind, scope, address).
*   **Second Pass (Code Generation):** With the complete symbol table, the compiler makes a second pass to generate the final code, correctly resolving all symbols.

### 2. Modular Components

The VM Translator and Compiler are broken down into logical, decoupled components:

*   **The Tokenizer (`JackTokenizer`):** Handles lexical analysis, breaking raw source code into a stream of tokens. It was enhanced with a `peek()` method to enable look-ahead parsing.
*   **The Parser/Engine (`CompilationEngine`):** A recursive descent parser that handles syntax analysis, applying the language's grammar rules to the token stream.
*   **The Symbol Table (`SymbolTable`):** Manages all semantic information, tracking identifier scopes (class, subroutine) and properties.
*   **The Code Generator (`VMWriter`):** Provides a clean API for writing the target language (VM code), decoupling the parser from the specifics of the output format.

---

## Example Program

A minimal single-file Jack program that demonstrates the pipeline:

**`examples/SimpleAdd/Main.jack`:**

```jack
class Main {
    function int add(int a, int b) {
        return a + b;
    }

    function void main() {
        do Output.printInt(Main.add(2, 3));
        return;
    }
}
```

This compiles to VM → ASM → Hack and prints `5` on the screen when run in the CPU Emulator.

---

## Requirements

*   Python 3.x
*   Official Nand2Tetris tools (for running `.hack` binaries)

---

## Roadmap

*   Add simple IDE frontend for Jack/VM/ASM side-by-side view
*   Add support for the Jack OS libraries (separate repo)
*   Optional: build higher-level demos (e.g., Tetris)

---

## Notes

This repository focuses **only** on the compiler toolchain. The Jack OS library and application-level programs (e.g., Tetris) will be in separate repositories.

Note:
The Jack OS library is not part of this repository and is provided by the official Nand2Tetris tools.
The end-to-end pipeline (Jack → VM → ASM → Hack) works fully when the OS .vm files are included.

To run your compiled code on the CPU emulator, copy the official OS .vm library files
into the output directory before running the VM translator and assembler.
