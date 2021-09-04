PRJ_NAME=latex_proj_tool

lint:
	python3 -m pylint ${PRJ_NAME} --rcfile=tests/lint/pylintrc

type:
	# intall-types is the new feature since mypy 0.900 that installs missing stubs.
	python3 -m mypy ${PRJ_NAME} --ignore-missing-imports --install-types --non-interactive

format:
	python3 -m black -l 100 `git diff --name-only --diff-filter=ACMRTUX origin/main -- "*.py" "*.pyi"`

check_format:
	python3 -m black -l 100 --check `git diff --name-only --diff-filter=ACMRTUX origin/main -- "*.py" "*.pyi"`

test:
	python3 -m pytest --lf

clean:
	rm -rf .coverage* *.xml *.log *.pyc *.egg-info tests/temp* test_* tests/*.pdf curr *.db
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name ".pytest_cache" -type d -exec rm -r {} +
	find . -name ".pkl_memoize_py3" -type d -exec rm -r {} +

