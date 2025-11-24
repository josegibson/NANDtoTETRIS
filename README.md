# Nand2Tetris Compiler Suite & Web IDE

## Overview

This repository contains a fully implemented, modular compiler toolchain for the **Jack programming language**, paired with a modern **Web-based IDE**. This project reproduces the entire **software pipeline** from a high-level, object-oriented language down to executable machine code for the Hack computer, and allows you to write, compile, and run Jack programs directly in your browser.

**Live Deployment:** [https://nand-compiler-web.onrender.com/](https://nand-compiler-web.onrender.com/)



## Features

*   **Web-Based IDE**: A modern React-based interface with Monaco Editor for writing Jack code.
*   **Full Compilation Pipeline**: Compiles Jack code through all stages:
    *   **Jack -> VM**: High-level code to Virtual Machine code.
    *   **VM -> Assembly**: VM code to Hack Assembly.
    *   **Assembly -> Hack**: Assembly to binary machine code.
*   **Integrated VM Emulator**: Run your compiled Jack programs directly in the browser with a fully functional VM emulator (screen and keyboard support).
*   **Split-Pane Interface**: View your source code alongside the generated VM, Assembly, and Binary output.
*   **Downloadable Artifacts**: Download the compiled files for use with local Nand2Tetris tools.
*   **Modular Architecture**: Clean separation between the compiler logic (Python) and the frontend interface (React/TypeScript).

---

## Project Structure

```
/server/         # Python Flask Backend & Compiler Logic
  /jack/         # Refactored Compiler Toolchain Package
  server.py      # Flask API Entry Point
/web/            # React + Vite Frontend
  /src/          # UI Components, VM Emulator, and Logic
/examples/       # Example Jack programs
```

---

## Getting Started (Local Development)

To run the project locally, you need to set up both the Python backend and the React frontend.

### Prerequisites

*   Node.js (v16+)
*   Python 3.x

### 1. Backend Setup

The backend handles the compilation logic.

```bash
cd server
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python server.py
```
The server will start on `http://localhost:5000`.

### 2. Frontend Setup

The frontend provides the IDE and VM emulator.

```bash
cd web
npm install
npm run dev
```
The web app will start on `http://localhost:5173`.

---

## Architecture

The project follows a client-server architecture:

*   **Frontend (Client)**: Built with **React**, **Vite**, and **TypeScript**. It handles the user interface, code editing (Monaco), and the **VM Emulator**. The emulator is implemented in TypeScript and runs the generated VM code directly in the browser, simulating the Hack computer's screen and memory.
*   **Backend (Server)**: Built with **Flask**. It exposes the Python compiler toolchain as an API. When you click "Compile", the Jack code is sent to the server, processed by the `jack` package, and the resulting VM/ASM/Hack code is returned to the client.

---

## Core Compiler Toolchain

The core compiler logic resides in `server/jack` and can still be used as a standalone command-line tool.

### Components

*   **The Tokenizer (`JackTokenizer`)**: Handles lexical analysis.
*   **The Parser (`CompilationEngine`)**: Recursive descent parser for syntax analysis.
*   **The Symbol Table (`SymbolTable`)**: Manages identifier scopes and properties.
*   **The Code Generator (`VMWriter`)**: Generates VM code.
*   **VM Translator**: Translates VM code to Assembly.
*   **Assembler**: Translates Assembly to Hack binary.

### Manual Usage

You can use the compiler logic directly from the command line:

```bash
# From the server/ directory
python -m jack.analyzer ../examples/SimpleAdd/
```

---

## Deployment

The project is configured for deployment on **Render**.
*   The `render.yaml` file defines the services.
*   The backend is deployed as a Python Web Service.
*   The frontend is deployed as a Static Site, rewriting API requests to the backend.

---

## Roadmap

*   [x] Web-based IDE
*   [x] Integrated VM Emulator
*   [x] Full Compilation Pipeline
*   [ ] Step-by-step Debugging
*   [ ] Syntax Highlighting for Jack (Custom Monaco Language)
*   [ ] User Accounts / Project Saving
