@echo off
REM coverage_for_class.bat
REM Usage: coverage_for_class.bat [module] [test_file]
REM Example: coverage_for_class.bat code2flow.model tests/test_variable.py

SETLOCAL

IF "%1"=="" (
  SET "MODULE=code2flow.model"
) ELSE (
  SET "MODULE=%~1"
)

IF "%2"=="" (
  SET "TESTFILE=tests/test_variable.py"
) ELSE (
  SET "TESTFILE=%~2"
)

echo Installing dev requirements (if any)...
IF EXIST requirements_dev.txt (
  python -m pip install -r requirements_dev.txt
) ELSE (
  echo requirements_dev.txt not found; ensure pytest-cov is installed
  python -m pip install pytest-cov
)

echo Running pytest with coverage for %MODULE% on %TESTFILE%...
pytest --cov=%MODULE% --cov-report=term-missing --cov-report=html:htmlcov %TESTFILE%
IF %ERRORLEVEL% NEQ 0 (
  echo pytest failed with exit code %ERRORLEVEL%.
  ENDLOCAL
  EXIT /B %ERRORLEVEL%
)

IF EXIST htmlcov\index.html (
  echo Opening HTML report...
  start "" htmlcov\index.html
) ELSE (
  echo HTML report not found in htmlcov\index.html
)

ENDLOCAL
