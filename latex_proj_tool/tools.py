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
A tool set to work on Latex projects.
"""
import glob
import os
import re

from .logger import get_logger


class TexVisitor:
    """Visit the .tex files recursively by \\input{} and run the given callback.

    Parameters
    ----------
    root_path: str
        The root .tex file path.
    """

    input_pattern = re.compile(r"\\input{(.*)}")

    def __init__(self, root_file_name: str):
        if root_file_name.find(" ") != -1:
            raise ValueError(f"Do not support file path with spaces: {root_file_name}")
        self.root_file_name = root_file_name
        self.root_path, _ = os.path.split(root_file_name)
        self.logger = get_logger(self.__class__.__name__)

    def visit(self, file_name: str):
        """Visit each .tex file and execute callbacks.

        Parameters
        ----------
        file_name: str
            The file name being visited.
        """
        file_name = file_name if file_name is not None else self.root_file_name

        self.file_callback(file_name)
        if not os.path.exists(file_name):
            self.logger.warning("File %s is missing", file_name)
            return

        with open(file_name, "r") as tex_file:
            for line in tex_file:
                if line.strip().startswith("%"):
                    continue
                match = self.input_pattern.search(line)
                if match:
                    input_file = match.group(1)
                    input_file += "" if input_file.endswith("tex") else ".tex"
                    self.visit(os.path.join(self.root_path, input_file))
                else:
                    self.line_callback(line)

    def run(self):
        """The entry point to start visiting."""
        raise NotImplementedError

    def line_callback(self, line: str):
        """The callback being executed for each visited line."""

    def file_callback(self, file_name: str):
        """The callback being executed f or each visited file."""


class TexFlatter(TexVisitor):
    """Flatten a Latex project to a single .tex file.

    Parameters
    ----------
    root_path: str
        The root .tex file path.

    out_file_name: str
        The output .tex file name.
    """

    def __init__(self, root_path: str, out_file_name: str):
        super().__init__(root_path)
        self.out_file_name = out_file_name
        self.out_file = None

    def run(self):
        with open(self.out_file_name, "w") as out_file:
            self.out_file = out_file
            self.visit(self.root_file_name)
        self.logger.info("The output has been written to %s", self.out_file_name)
        self.out_file = None

    def line_callback(self, line: str):
        assert self.out_file is not None
        self.out_file.write(line)

    def file_callback(self, file_name: str):
        self.logger.info("Visit %s", file_name)


class UnusedFileFinder(TexVisitor):
    """Log unused files in the project.

    Parameters
    ----------
    root_path: str
        The root .tex file path.
    """

    patterns = [re.compile(r"\\includegraphics.*{(.*)}"), re.compile(r"\\bibliography{(.*)}")]

    def __init__(self, root_file_name: str, exclude_dirs: str, exclude_extensions: str):
        super().__init__(root_file_name)
        all_files = set(glob.glob(f"{self.root_path}/**/*", recursive=True))
        self.exclude_dirs = (
            tuple(
                self.canonicalize_path(os.path.join(self.root_path, d))
                for d in exclude_dirs.split(",")
            )
            if exclude_dirs
            else ()
        )

        exclude_extension_tuple = tuple(
            e if e.startswith(".") else f".{e}" for e in exclude_extensions.split(",")
        )

        # Create a mapping from file path without extension to the complete file path.
        # Filer do-not-care files.
        self.unused_files = {
            self.canonicalize_path(f, remove_extension=True): self.canonicalize_path(
                f, remove_extension=False
            )
            for f in all_files
            if not os.path.isdir(f) and not f.endswith(exclude_extension_tuple)
        }

    @staticmethod
    def canonicalize_path(file_path: str, remove_extension: bool = True):
        path = os.path.abspath(file_path)
        if remove_extension:
            last_dot = path.rfind(".")
            if last_dot != -1 and path[last_dot + 1 :].find("/") == -1:
                path = path[:last_dot]

        return path

    def run(self):
        self.visit(self.root_file_name)
        unuseds = []
        for unused in self.unused_files.values():
            if self.exclude_dirs and unused.startswith(self.exclude_dirs):
                continue
            unuseds.append(unused)
            self.logger.info("Unused file: %s", os.path.relpath(unused))
        self.logger.info("Total %d unused files", len(unuseds))
        return unuseds

    def line_callback(self, line: str):
        for pattern in self.patterns:
            match = pattern.search(line)
            if match:
                file_name_wo_extension = self.canonicalize_path(
                    os.path.join(self.root_path, match.group(1)), remove_extension=True
                )
                if file_name_wo_extension in self.unused_files:
                    del self.unused_files[file_name_wo_extension]
                break

    def file_callback(self, file_name: str):
        file_wo_extension = self.canonicalize_path(file_name, remove_extension=True)
        if file_wo_extension in self.unused_files:
            del self.unused_files[file_wo_extension]
