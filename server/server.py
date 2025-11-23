import os
import sys
import subprocess
import tempfile
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Path to the root of the repository
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPILER_DIR = os.path.join(REPO_ROOT, 'Compiler')
VM_TRANSLATOR_DIR = os.path.join(REPO_ROOT, 'VMTranslator')
ASSEMBLER_DIR = os.path.join(REPO_ROOT, 'Assembler')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/compile', methods=['POST'])
def compile_project():
    """
    Accepts a JSON object with a list of files:
    {
        "files": [
            {"name": "Main.jack", "content": "..."},
            {"name": "Square.jack", "content": "..."}
        ]
    }
    Returns:
    {
        "vm": [{"name": "Main.vm", "content": "..."}],
        "asm": "...",
        "hack": "...",
        "error": "..." (optional)
    }
    """
    data = request.json
    if not data or 'files' not in data:
        return jsonify({'error': 'No files provided'}), 400

    # Create a temporary directory for processing
    temp_dir = tempfile.mkdtemp(prefix='nand_compiler_')
    
    try:
        # 1. Write Jack files to temp dir
        for file in data['files']:
            file_path = os.path.join(temp_dir, file['name'])
            with open(file_path, 'w') as f:
                f.write(file['content'])
        
        # 2. Run Jack Compiler (Jack -> VM)
        # Output VM files to the same directory
        jack_analyzer_script = os.path.join(COMPILER_DIR, 'JackAnalyzer.py')
        try:
            subprocess.run(
                [sys.executable, jack_analyzer_script, temp_dir, '--output', temp_dir],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            return jsonify({'error': f"Jack Compilation Failed:\n{e.stderr}"}), 400

        # Read generated VM files
        vm_files = []
        for f in os.listdir(temp_dir):
            if f.endswith('.vm'):
                with open(os.path.join(temp_dir, f), 'r') as vm_file:
                    vm_files.append({'name': f, 'content': vm_file.read()})
        
        if not vm_files:
             return jsonify({'error': "No VM files generated"}), 400

        # 3. Run VM Translator (VM -> ASM)
        # VMTranslator/main.py takes the directory as input and produces a .asm file
        vm_translator_script = os.path.join(VM_TRANSLATOR_DIR, 'main.py')
        try:
            subprocess.run(
                [sys.executable, vm_translator_script, temp_dir],
                check=True,
                capture_output=True,
                text=True,
                cwd=temp_dir
            )
        except subprocess.CalledProcessError as e:
             return jsonify({'error': f"VM Translation Failed:\n{e.stderr}"}), 400

        # Find the generated ASM file
        asm_content = ""
        asm_filename = os.path.basename(temp_dir) + ".asm" # VMTranslator usually names it after the dir
        # However, the repo's VMTranslator might name it differently. 
        # Let's look for any .asm file
        found_asm = False
        for f in os.listdir(temp_dir):
            if f.endswith('.asm'):
                with open(os.path.join(temp_dir, f), 'r') as asm_file:
                    asm_content = asm_file.read()
                    asm_filename = f
                    found_asm = True
                    break
        
        if not found_asm:
             return jsonify({'error': "No ASM file generated"}), 400

        # 4. Run Assembler (ASM -> Hack)
        assembler_script = os.path.join(ASSEMBLER_DIR, 'main.py')
        asm_file_path = os.path.join(temp_dir, asm_filename)
        try:
            subprocess.run(
                [sys.executable, assembler_script, asm_file_path],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
             return jsonify({'error': f"Assembly Failed:\n{e.stderr}"}), 400

        # Find the generated Hack file
        hack_content = ""
        for f in os.listdir(temp_dir):
            if f.endswith('.hack'):
                with open(os.path.join(temp_dir, f), 'r') as hack_file:
                    hack_content = hack_file.read()
                    break
        
        return jsonify({
            'vm': vm_files,
            'asm': asm_content,
            'hack': hack_content
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
