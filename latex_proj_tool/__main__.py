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
The CLI entry.
"""
import argparse
from .logger import get_logger
from . import tools

logger = get_logger("Main")


def create_config():
    """Create the CLI configuration.

    Returns
    -------
    ArgumentParser:
        The parsed commandline arguments.
    """
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("root", help="The LaTex project main .tex file")

    main_parser = argparse.ArgumentParser()
    subprasers = main_parser.add_subparsers(dest="operation", help="The operation to be performed")

    flatter_parser = subprasers.add_parser(
        "flat",
        parents=[parent_parser],
        help="Flat all .tex files in the project to a single .tex file",
    )
    flatter_parser.add_argument("--output", "-o", default="out.tex", help="The output .tex file")

    unused_parser = subprasers.add_parser(
        "find_unused", parents=[parent_parser], help="List all unused files in the project"
    )
    unused_parser.add_argument(
        "--exclude-dirs",
        default="",
        help="The directories (relative path to the project root) we do not care. "
        "Separate by comma.",
    )
    unused_parser.add_argument(
        "--exclude-extensions",
        default="",
        help="The file extensions we do not care. Separate by comma",
    )

    return main_parser.parse_args()


def main():
    """The main entry."""
    config = create_config()

    if config.operation == "flat":
        tools.TexFlatter(config.root, config.output).run()
    elif config.operation == "find_unused":
        tools.UnusedFileFinder(config.root, config.exclude_dirs, config.exclude_extensions).run()
    else:
        logger.error("Unrecognized operation: %s", config.operation)


if __name__ == "__main__":
    main()
