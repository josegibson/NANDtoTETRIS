import os, sys, pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import VMTranslator

input_path = os.path.join(os.path.dirname(__file__), "project_docs")
output_path = os.path.join(os.path.dirname(__file__), "output")
expected_output_path = os.path.join(os.path.dirname(__file__), "expected_output")

tests = [
    "BasicTest",
    "PointerTest",
    "SimpleAdd",
    "StackTest",
    "StaticTest",
    "BasicLoop",
    "FibonacciSeries",
    "SimpleFunction",
    "NestedCall",
    "FibonacciElement"
]

@pytest.mark.parametrize("test_name", tests)
def test_vmt(test_name):


    input = os.path.join(input_path, f"{test_name}")
    vmt = VMTranslator(dest_dir=output_path)
        
    vmt.run(input)


    # Testing with expected result
    output = os.path.join(output_path, f'{test_name}.asm')
    expected_output = os.path.join(expected_output_path, f"{test_name}.asm")

    out = ""
    with open(output) as f:
        out = f.read()

    expected_out = ""
    with open(expected_output) as f:
        expected_out = f.read()

    # Use the Parser.clean if needed to remove spaces and comments later!
    assert out == expected_out

