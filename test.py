import os
import builtins
from datetime import datetime
import subprocess
import difflib
from pprint import pprint

# get the function to test
import Main

# store these in the local scope
# DO NOT REMOVE THESE TWO LINES
input = input
print = print

# get teh list of all test folders, exlcude files via name
test_folders = [item for item in os.listdir('tests') if '.' not in item]

# silence default print output
# later this could be logged into a list but i can;t be bothered rn
# builtins.print = lambda *_, **__: None


for testname in test_folders:

    print(f"testing `tests/{testname}` ...")

    out_filename = Main.filename(call=testname)
    # if this validation becomes tedious, comment this out (keep the delete)
    input(f"deleting {out_filename} ... (hit ctrl-c to cancel test)")
    os.remove(out_filename)
    print("delted")

    with open(f"tests/{testname}/in.txt") as infile:
        # define a test function tha treplaces the default input statement
        def test_input(prompt:str) -> str:
            line = infile.readline()

            try:
                if line.endswith('\n'):
                    return line[0:-1].replace('[TAB]', '\t') # return the line w/out the trailing return
                elif line == '': # if there are not more lines to read
                    raise RuntimeError(
                        "the program being tested is asking form more input than "
                        f"the `tests/{testname}` test can provide "
                        "(reached end fo file w/out exit working)"
                    )
                else:
                    assert False, (
                        "this line should be unreachable as .readline() should "
                        f"either be '' or end with a newline, got {repr(line)}"
                    )
            except Exception as err:
                print("OMG THERE WAS AN ERROR in the replace input() fn")
                raise err

        # substiture this test_input for the std input
        builtins.input = test_input

        # then call the main function
        Main.main()
    print(f"main over")
    #write out a temporary out file with proper tabbing:
    test_against = f"tests/{testname}/out.tabbed.tmp"
    differ = difflib.Differ()
    lineno = 0
    with open(out_filename) as outirl, open(f"tests/{testname}/out.txt") as outfmt:
        lineno += 1
        outirl.readline() == 

    print("Bye Bye")
