# The NAND to TETRIS Compiler Suite

### **Overview**

This repository contains my complete, modern implementation of the NAND to TETRIS software suite. This project is not just a single program but a full suite of language translation tools, built from the ground up to demonstrate the entire compilation pipeline from a high-level, object-oriented language down to executable machine code.

The suite is composed of three distinct, yet interconnected, components:

1.  **The Assembler:** Translates symbolic Hack Assembly language into binary machine code.
2.  **The VM Translator:** Translates a high-level, stack-based virtual machine language into Hack Assembly.
3.  **The Jack Compiler:** A full-featured compiler for the "Jack" language—a high-level, object-oriented language similar to Java—that compiles Jack source code into the VM language.

The complete compilation pipeline can be visualized as follows:

```
             Compiler            VM            Assembler
Source Code ---------> Bytecode ----> Assembly --------> Binary
````

### **Key Architectural Highlights**

This project was built with a focus on clean architecture, modularity, and robust design patterns common in modern compiler construction.

#### **1. Two-Pass Compiler Architecture**

Both the Assembler and the final Jack Compiler are built using a **two-pass architecture**. This design is fundamental to solving the problem of **forward references** (e.g., using a variable or calling a function before it has been declared).

* **First Pass (Symbol Table Construction):** The compiler makes an initial pass through the source code with the sole purpose of building a complete **Symbol Table**. This table maps every identifier (variable, label, subroutine name) to its semantic properties (type, kind, scope, address).
* **Second Pass (Code Generation):** With the completed symbol table, the compiler makes a second pass to generate the final code. It now has the full context needed to correctly resolve all symbols.

#### **2. Modular, Single-Responsibility Design**

The VM Translator and Compiler are broken down into logical, decoupled components, each with a single responsibility:

* **The Tokenizer (`JackTokenizer`):** Handles lexical analysis, breaking the raw source code into a stream of tokens. It was enhanced with a `peek()` method to enable look-ahead parsing.
* **The Parser/Engine (`CompilationEngine`):** A recursive descent parser that handles syntax analysis, applying the language's grammar rules to the token stream.
* **The Symbol Table (`SymbolTable`):** Manages all semantic information, tracking identifier scopes and properties.
* **The Code Generator (`VMWriter`):** Provides a clean API for writing the target language (VM code), decoupling the parser from the specifics of the output format.

### **How to Use the Jack Compiler**

The main entry point for the compiler is the `JackAnalyzer.py` script. It is a command-line tool designed to compile a single `.jack` file or an entire directory of `.jack` files.

#### **Prerequisites**

* Python 3.x

#### **Execution**

Navigate to the `Compiler/` directory and run the analyzer from your terminal.

```bash
# Navigate to the Compiler directory
cd Compiler/

# Run the analyzer on a source file or directory
python JackAnalyzer.py <path/to/source.jack_or_directory>
````

#### **Command-Line Arguments**

The analyzer accepts several optional flags to control its behavior:

  * `--output <directory>`: Specify a directory to write the output `.vm` files to. If omitted, the output is not saved.
  * `-m, --mode [vm|xml]`: Choose the output mode. Defaults to `vm` for code generation. Use `xml` to generate a parse tree for debugging.
  * `-v, -vv, -vvv`: Increase the output verbosity for debugging.
      * `-v`: Prints class-level scope information.
      * `-vv`: Also prints subroutine-level scope information.
      * `-vvv`: Also prints the generated VM code for each subroutine.

**Example:**

```bash
# Compile the entire 'Pong' project and see full debug output
python JackAnalyzer.py ../projects/11/Pong -vvv --output ../compiled_output/
```

### Future Vision & Roadmap
This compiler suite serves as the robust back-end for a planned interactive educational tool. The next phase of the project is to build a simple front-end that will leverage this engine to provide:

- A multi-pane editor to show Jack, VM, and Assembly code side-by-side.
- 
- A visual simulation of the stack and memory segments as the VM code executes.