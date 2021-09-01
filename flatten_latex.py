"""
A simple script to flatten a Latex project with multiple .tex files.
Then it can be used by other Latex tools such as latexdiff.

Usage: python3 flatten_latex.py my_project/main.tex out.tex
"""
import sys
import os
import re


def flatten(root_file_name: str, out_file_name: str):
    """Flatten a Latex project to a single .tex file.

    Parameters
    ----------
    root_file_name: str
        The root .tex file path.

    out_file_name: str
        The output .tex file name.
    """
    input_pattern = re.compile(r"^\\input{(.*)}")
    root_path, _ = os.path.split(root_file_name)

    with open(out_file_name, "w") as out_file:

        def flatten_helper(file_name):
            with open(file_name, "r") as tex_file:
                for line in tex_file:
                    match = input_pattern.search(line)
                    # If this line starts with \input, then flatten its contents.
                    if match:
                        input_file = match.group(1)
                        print("Flatten %s" % input_file)
                        input_file += "" if input_file.endswith("tex") else ".tex"
                        flatten_helper(os.path.join(root_path, input_file))
                    else:
                        out_file.write(line)

        flatten_helper(root_file_name)


if __name__ == "__main__":
    flatten(sys.argv[1], sys.argv[2])
