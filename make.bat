@echo off
setlocal

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="clean" goto clean
if "%1"=="install" goto install
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="lint-netgsm" goto lint-netgsm
if "%1"=="lint-tests" goto lint-tests
if "%1"=="lint-examples" goto lint-examples
if "%1"=="format" goto format
if "%1"=="format-netgsm" goto format-netgsm
if "%1"=="format-tests" goto format-tests
if "%1"=="format-examples" goto format-examples
if "%1"=="build" goto build
if "%1"=="publish" goto publish

:help
echo clean      - remove all build, test, coverage and Python artifacts
echo install    - install the package to the active Python's site-packages
echo test       - run tests with pytest
echo lint       - check style with flake8 and black (all)
echo format     - format code with black (all)
echo build      - package
echo publish    - package and upload a release
goto :eof

:clean
py -c "import shutil; import glob; import os; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dist', '*.egg-info', '.coverage', 'htmlcov', '.pytest_cache', '.tox'] + glob.glob('**/__pycache__', recursive=True)]"
py -c "import glob; import os; [os.remove(f) for f in glob.glob('**/*.py[cod]', recursive=True)]"
goto :eof

:install
py -m pip install --upgrade pip
py -m pip install -e ".[dev]"
py -m pip install black flake8 pytest pytest-cov
goto :eof

:test
py -m pytest --verbose --color=yes
goto :eof

:lint
call :lint-netgsm
call :lint-tests
call :lint-examples
goto :eof

:lint-netgsm
py scripts/lint.py netgsm
goto :eof

:lint-tests
py scripts/lint.py tests
goto :eof

:lint-examples
py scripts/lint.py examples
goto :eof

:format
call :format-netgsm
call :format-tests
call :format-examples
goto :eof

:format-netgsm
py scripts/format.py netgsm
goto :eof

:format-tests
py scripts/format.py tests
goto :eof

:format-examples
py scripts/format.py examples
goto :eof

:build
call :clean
py setup.py sdist bdist_wheel
goto :eof

:publish
call :build
py -m twine check dist/*
py -m twine upload dist/*
goto :eof 