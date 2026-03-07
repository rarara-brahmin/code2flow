cd /d %~dp0
@REM call venv\Scripts\activate
python -m code2flow tests\test_code\py\exclude_modules_two_files\exclude_modules_a.py -o out\exclude_modules_a.svg
python -m code2flow tests\test_code\py\exclude_modules_two_files\exclude_modules_a.py -o out\exclude_modules_a_showL.svg --show-libraries
python -m code2flow tests\test_code\py\import_paths\import_paths.py -o out\import_paths.svg
python -m code2flow tests\test_code\py\import_paths\import_paths.py -o out\import_paths_showL.svg --show-libraries
python -m code2flow tests\test_code\py\inherits\inherits.py -o out\inherits.svg
python -m code2flow tests\test_code\py\inherits\inherits.py -o out\inherits_showL.svg --show-libraries
python -m code2flow tests\test_code\py\init\init.py -o out\init.svg
python -m code2flow tests\test_code\py\init\init.py -o out\init_showL.svg --show-libraries
python -m code2flow tests\test_code\py\nested_calls\nested_calls.py -o out\nested_calls.svg
python -m code2flow tests\test_code\py\nested_calls\nested_calls.py -o out\nested_calls_showL.svg --show-libraries
python -m code2flow tests\test_code\py\nested_calls\nested_calls.py -o out\nested_calls_nohu.svg
python -m code2flow tests\test_code\py\nested_calls\nested_calls.py -o out\nested_calls_nohu_showL.svg --show-libraries
python -m code2flow tests\test_code\py\nested_class\nested_class.py -o out\nested_class.svg
python -m code2flow tests\test_code\py\nested_class\nested_class.py -o out\nested_class_showL.svg --show-libraries
python -m code2flow tests\test_code\py\pytz\__init__.py -o out\pytz__init__.svg
python -m code2flow tests\test_code\py\pytz\__init__.py -o out\pytz__init__showL.svg --show-libraries
python -m code2flow code2flow -o out\code2flow.svg level=logging.DEBUG
python -m code2flow code2flow -o out\code2flow_showL.svg --show-libraries 

pause
