
import os, sys, pytest, glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from JackAnalyzer import JackAnalyzer


project_path = 'D:\\NANDtoTETRIS\\projects\\10'
test_path = os.path.join(os.path.dirname(__file__), 'outputs')
@pytest.mark.parametrize("testname", os.listdir(project_path))
def test_compiler(testname):
    os.makedirs(os.path.join(test_path, testname), exist_ok=True)
    ja = JackAnalyzer(os.path.join(project_path, testname), os.path.join(test_path, testname))

    xmlfiles = [os.path.basename(i) for i in glob.glob(os.path.join(test_path, testname, '*.xml'))]

    for xmlfile in xmlfiles:
        comparedata = None
        outputdata = None

        with open(os.path.join(test_path, testname, xmlfile), 'r') as f:
            outputdata = f.read()
        

        with open(os.path.join(project_path, testname, xmlfile), 'r') as f:
            comparedata = f.read()

        assert comparedata == outputdata
        
    

    

