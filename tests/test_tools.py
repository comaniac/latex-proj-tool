"""
The unit tests.
"""
import os
import pytest
import tempfile
from latex_proj_tool.tools import TexFlatter, UnusedFileFinder


def test_flatter():
    with tempfile.TemporaryDirectory(prefix="latex_proj_tool_test_", dir="/tmp") as tmpdir:
        root_path = os.path.join(tmpdir, "main.tex")
        with open(root_path, "w") as fp:
            fp.write("aaa\n\\input{b.tex}\n")

        with open(os.path.join(tmpdir, "b.tex"), "w") as fp:
            fp.write("bbb\n  \\input{c.tex}  ")

        with open(os.path.join(tmpdir, "c.tex"), "w") as fp:
            fp.write("ccc\n  %\\input{d.tex}")

        out_file = os.path.join(tmpdir, "out.tex")
        TexFlatter(root_path, out_file_name=out_file).run()
        with open(out_file, "r") as fp:
            assert fp.read() == "aaa\nbbb\nccc\n"

        with open(os.path.join(tmpdir, "c.tex"), "w") as fp:
            fp.write("ccc\n  \\input{d.tex}")

        TexFlatter(root_path, out_file_name=out_file).run()
        with open(out_file, "r") as fp:
            assert fp.read() == "aaa\nbbb\nccc\n"


def test_unused():
    with tempfile.TemporaryDirectory(prefix="latex_proj_tool_test_", dir="/tmp") as tmpdir:
        root_path = os.path.join(tmpdir, "main.tex")
        with open(root_path, "w") as fp:
            fp.write("\\input{b.tex}\n")
            fp.write(" \\includegraphics{fig1.pdf}\n")
            fp.write(" \\bibliography{./ref}\n")

        with open(os.path.join(tmpdir, "b.tex"), "w") as fp:
            fp.write(" \\includegraphics[width=0.8\linewidth]{./figure/fig2.pdf}\n")

        os.mkdir(os.path.join(tmpdir, "exclude"))
        os.mkdir(os.path.join(tmpdir, "figure"))
        for file_name in [
            "fig1.pdf",
            "figure/fig2.pdf",
            "ref.bib",
            "format.bst",
            "my.sty",
            "unused1.tex",
            "unused2.pdf",
            "exclude/a.tex",
        ]:
            with open(os.path.join(tmpdir, file_name), "w") as fp:
                fp.write("placeholder\n")

        unuseds = UnusedFileFinder(root_path, "exclude", ".sty,bst").run()
        assert len(unuseds) == 2
        assert all(["unused" in f for f in unuseds])


if __name__ == "__main__":
    pytest.main([__file__])
