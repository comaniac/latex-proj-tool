# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
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
