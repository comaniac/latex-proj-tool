# Latex Flatter
Flatten a Latex project to a single .tex file. This is useful if you want to
use latexdiff or other Latex tools that require a single .tex file.

This is mainly inspired by
this post: http://dropbearcode.blogspot.com/2011/09/multiple-file-latex-diff.html

## Usage

```bash
python3 flatten_latex.py my_project/main.tex out.tex
```

## Application: latexdiff

### Steup
1. Make sure you have Perl 5.8+ in your environment.
2. Download `latexdiff` from https://www.ctan.org/tex-archive/support/latexdiff

### Steps
1. `unzip latexdiff`
2. `python3 flatten_latex.py old_project/main.tex old.tex`
3. `python3 flatten_latex.py new_project/main.tex new.tex`
4. `latexdiff old.tex new.tex > temp.tex`
5. `sed 's/^M//' tmp.tex > diff.tex`
6. Compile `diff.tex` to get the PDF.

