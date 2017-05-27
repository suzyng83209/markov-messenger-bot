rapydscript -b -p -m hello.py > hello.js
rm -r compiledpythonextension/hello.js
mv hello.js compiledpythonextension
