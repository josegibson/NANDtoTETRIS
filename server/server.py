import os
import sys
import tempfile
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import the jack compiler module
from jack.Compiler.JackAnalyzer import JackAnalyzer
from jack.VMTranslator.main import VMTranslator
from jack.Assembler.main import assemble_file

app = Flask(__name__)
CORS(app)

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
        # Use JackAnalyzer directly instead of subprocess
        try:
            JackAnalyzer(temp_dir, temp_dir, mode='vm', verbose=0)
        except Exception as e:
            return jsonify({'error': f"Jack Compilation Failed:\n{str(e)}"}), 400

        # Read generated VM files
        vm_files = []
        for f in os.listdir(temp_dir):
            if f.endswith('.vm'):
                with open(os.path.join(temp_dir, f), 'r') as vm_file:
                    vm_files.append({'name': f, 'content': vm_file.read()})
        
        if not vm_files:
             return jsonify({'error': "No VM files generated"}), 400

        # 3. Run VM Translator (VM -> ASM)
        # Use VMTranslator directly instead of subprocess
        try:
            vmt = VMTranslator(dest_dir=temp_dir)
            vmt.run(temp_dir)
        except Exception as e:
             return jsonify({'error': f"VM Translation Failed:\n{str(e)}"}), 400

        # Find the generated ASM file
        asm_content = ""
        asm_filename = os.path.basename(temp_dir) + ".asm"
        # Look for any .asm file
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
        # Use assemble_file directly instead of subprocess
        asm_file_path = os.path.join(temp_dir, asm_filename)
        try:
            hack_file_path = assemble_file(asm_file_path)
        except Exception as e:
             return jsonify({'error': f"Assembly Failed:\n{str(e)}"}), 400

        # Read the generated Hack file
        hack_content = ""
        if os.path.exists(hack_file_path):
            with open(hack_file_path, 'r') as hack_file:
                hack_content = hack_file.read()
        
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
