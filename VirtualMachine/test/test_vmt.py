

import os, sys

sys.path.insert(0, "D:\\NANDtoTETRIS\\VirtualMachine")

from main import VMTranslator

input_path = os.path.join(os.path.dirname(__file__), "project_docs")
output_path = os.path.join(os.path.dirname(__file__), "output")
expected_output_path = os.path.join(os.path.dirname(__file__), "expected_output")


def test_translation(test_id=None):
    vmt = VMTranslator()
    vmt.translate(os.path.join(input_path, "BasicTest", "BasicTest.vm"), outdir=output_path)

