$password = 'AqWHkqpMpfLK9RuF'
python -m venv .env
.env/Scripts/activate
python -m pip install -r requirements.txt
pyarmor register ./pyarmor-regcode-3271.txt
pyarmor obfuscate -r prism/__init__.py --platform windows.x86_64 --output=dist/prism/
cp setup.py dist/
cd dist/
python setup.py sdist bdist_wheel
rm -r ../.env
# twine upload dist/* -u Prism39 -p $password
# cd ..
# rm -r dist/