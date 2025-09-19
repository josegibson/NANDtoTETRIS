import os, sys, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import VMTranslator

input_path = os.path.join(os.path.dirname(__file__), "project_docs")
output_path = os.path.join(os.path.dirname(__file__), "output")
expected_output_path = os.path.join(os.path.dirname(__file__), "expected_output")


@pytest.mark.parametrize("test_name", [
    "BasicTest",
    "PointerTest",
    "SimpleAdd",
    "StackTest",
    "StaticTest",
    'BasicLoop'
])
def test_translation(test_name):

    input = os.path.join(input_path, f"{test_name}", f"{test_name}.vm")
    output = os.path.join(output_path, f'{test_name}.asm')
    expected_output = os.path.join(expected_output_path, f"{test_name}.asm")

    vmt = VMTranslator()
        
    vmt.translate(input, outdir=output_path)

    out = ""
    with open(output) as f:
        out = f.read()

    expected_out = ""
    with open(expected_output) as f:
        expected_out = f.read()

    # Use the Parser.clean if needed to remove spaces and comments later!
    assert out == expected_out

