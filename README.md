# Latex Project Managment Tool

[![Build](https://github.com/comaniac/latex-proj-tool/actions/workflows/build.yml/badge.svg)](https://github.com/comaniac/latex-proj-tool/actions/workflows/build.yml)

A toolset to traverse and manipulate a Latex project with multiple .tex files.
Here are the currently supported functionalities. You are welcome to contribute more features :)

## Project flatten

Flatten a Latex project to a single .tex file. This is useful if you want to
use latexdiff or other Latex tools that require a single .tex file.

This is mainly inspired by
this post: http://dropbearcode.blogspot.com/2011/09/multiple-file-latex-diff.html

### Usage with latexdiff

1. Make sure you have Perl 5.8+ in your environment.
2. Download `latexdiff` from https://www.ctan.org/tex-archive/support/latexdiff
3. `unzip latexdiff`
4. `python3 -m latex_proj_tool flat old_project/main.tex old.tex`
5. `python3 -m latex_proj_tool flat new_project/main.tex new.tex`
6. `latexdiff old.tex new.tex > temp.tex`
7. `sed 's/^M//' tmp.tex > diff.tex`
8. Compile `diff.tex` to get the PDF.

## List Unused Files

List all unused files to help you clean the project.

### Usage

List all unused files in this project:
```
python3 -m latex_proj_tool find_unused my_project/main.tex
```

List all unused files in this project, excluding some files:
```
python3 -m latex_proj_tool find_unused my_project/main.tex --exclude-extensions cls,sty,bst
```

List all unused files in this project, excluding some directories:
```
python3 -m latex_proj_tool find_unused my_project/main.tex --exclude-dirs backup
```
