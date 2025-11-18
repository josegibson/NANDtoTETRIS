import os
import sys
import argparse
import tempfile
import shutil
import subprocess


def compile_jack_to_hack(input_path, output_dir, keep_temp=True, verbose=0):
    """Run the repository pipeline to compile a .jack file (or all .jack in a dir)
    into a .hack file in output_dir.

    Steps (uses existing scripts in the repo):
    1. Run Compiler/JackAnalyzer.py to produce a .vm file into a temporary dir
    2. Run VirtualMachine/main.py with cwd=output_dir to translate the .vm -> .asm
    3. Run Assembler/main.py to assemble the .asm -> .hack
    """

    # base directory of this script (repo root)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # collect jack files
    jack_files = []
    if os.path.isdir(input_path):
        for f in os.listdir(input_path):
            if f.lower().endswith('.jack'):
                jack_files.append(os.path.join(input_path, f))
    elif os.path.isfile(input_path) and input_path.lower().endswith('.jack'):
        jack_files.append(input_path)
    else:
        raise ValueError('Input must be a .jack file or directory containing .jack files')

    tempdir = None
    # If keep_temp is True, write .vm files directly into the output_dir so
    # they remain next to the generated .asm/.hack. Otherwise write them to a
    # temporary directory which will be removed at the end.
    if not keep_temp:
        tempdir = tempfile.mkdtemp(prefix='jack_vm_tmp_', dir=os.getcwd())
    try:
        # If the input is a directory, generate all VM files first and then
        # run the VM translator once on the VM output directory so a single
        # combined .asm (and .hack after assembling) is produced.
        if os.path.isdir(input_path):
            # 1) Generate .vm for each .jack into vm_out_dir
            # Call the JackAnalyzer once with the input directory so it can
            # process all .jack files in a single run (JackAnalyzer supports
            # directory inputs).
            vm_out_dir = output_dir if keep_temp else tempdir
            if verbose:
                print(f"[1/3] Generating .vm for directory {input_path} -> {vm_out_dir}")
            subprocess.run([sys.executable, os.path.join(script_dir, 'Compiler','JackAnalyzer.py'), input_path, '--output', vm_out_dir, '-m', 'vm'], check=True)

            # Verify at least one vm file exists
            vm_files = [f for f in os.listdir(vm_out_dir) if f.lower().endswith('.vm')]
            if not vm_files:
                raise FileNotFoundError(f'No VM files generated in: {vm_out_dir}')

            # 2) Translate the entire VM directory -> single .asm
            if verbose:
                print(f"[2/3] Translating .vm -> .asm: {vm_out_dir} -> {output_dir}")
            # Run VM translator once, with cwd=output_dir so the .asm is written there
            subprocess.run([sys.executable, os.path.join(script_dir, 'VirtualMachine','main.py'), vm_out_dir], cwd=output_dir, check=True)

            # Determine asm and hack filenames based on the input directory name
            project_name = os.path.basename(os.path.normpath(input_path))
            asmfile = os.path.join(output_dir, project_name + '.asm')
            if not os.path.exists(asmfile):
                raise FileNotFoundError(f'Expected ASM file not found: {asmfile}')

            # 3) Assemble the combined .asm -> single .hack
            if verbose:
                print(f"[3/3] Assembling .asm -> .hack: {asmfile}")
            subprocess.run([sys.executable, os.path.join(script_dir, 'Assembler','main.py'), asmfile], check=True)

            hackfile = os.path.join(output_dir, project_name + '.hack')
            if not os.path.exists(hackfile):
                raise FileNotFoundError(f'Expected HACK file not found: {hackfile}')

            if verbose:
                print(f"Done: {hackfile}")

        else:
            # Single-file flow (unchanged): produce per-file .vm/.asm/.hack
            for jackfile in jack_files:
                base = os.path.splitext(os.path.basename(jackfile))[0]

                # 1) Jack -> .vm
                vm_out_dir = output_dir if keep_temp else tempdir
                if verbose:
                    print(f"[1/3] Generating .vm for {jackfile} -> {vm_out_dir}")
                subprocess.run([sys.executable, os.path.join(script_dir, 'Compiler','JackAnalyzer.py'), jackfile, '--output', vm_out_dir, '-m', 'vm'], check=True)

                vmfile = os.path.join(vm_out_dir, base + '.vm')
                if not os.path.exists(vmfile):
                    raise FileNotFoundError(f'Expected VM file not found: {vmfile}')

                # 2) .vm -> .asm (run VM translator with cwd=output_dir so asm is written there)
                if verbose:
                    print(f"[2/3] Translating .vm -> .asm: {vmfile} -> {output_dir}")
                subprocess.run([sys.executable, os.path.join(script_dir, 'VirtualMachine','main.py'), vmfile], cwd=output_dir, check=True)

                asmfile = os.path.join(output_dir, base + '.asm')
                if not os.path.exists(asmfile):
                    raise FileNotFoundError(f'Expected ASM file not found: {asmfile}')

                # 3) .asm -> .hack (assemble)
                if verbose:
                    print(f"[3/3] Assembling .asm -> .hack: {asmfile}")
                subprocess.run([sys.executable, os.path.join(script_dir, 'Assembler','main.py'), asmfile], check=True)

                hackfile = os.path.join(output_dir, base + '.hack')
                if not os.path.exists(hackfile):
                    raise FileNotFoundError(f'Expected HACK file not found: {hackfile}')

                if verbose:
                    print(f"Done: {hackfile}")

    finally:
        # remove tempdir only when we used it for VM output
        if not keep_temp:
            try:
                shutil.rmtree(tempdir)
            except Exception:
                if verbose:
                    print(f"Could not remove temporary directory: {tempdir}")
        else:
            if verbose:
                print(f"VM files written to: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Compile .jack files to .hack using repository pipeline')
    parser.add_argument('input', help='Path to a .jack file or directory containing .jack files')
    parser.add_argument('--output', '-o', default='.', help='Directory to write .vm/.asm/.hack files (default: current directory)')
    parser.add_argument('--clean-temp', action='store_true', help='Remove temporary directory for intermediate .vm files (writes .vm to temp and deletes it)')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity')

    args = parser.parse_args()

    input_path = args.input
    output_dir = args.output

    # By default we keep VM files by writing them into the output directory.
    compile_jack_to_hack(input_path, output_dir, keep_temp=not args.clean_temp, verbose=args.verbose)


if __name__ == '__main__':
    main()
