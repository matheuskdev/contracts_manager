@echo off

echo Running isort...
isort .
if %errorlevel% neq 0 (
    echo isort found issues.
    exit /b %errorlevel%
)

echo Running Black...
black .
if %errorlevel% neq 0 (
    echo Black found issues.
    exit /b %errorlevel%
)

echo Running Flake8...
flake8 .
if %errorlevel% neq 0 (
    echo Flake8 found issues.
    exit /b %errorlevel%
)

echo All checks passed successfully!
