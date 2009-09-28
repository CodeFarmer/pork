clean : 
	rm -rf *.pyc classes/org/joellercoaster/*.class reference-classes/* *.tokens *Lexer.py *Parser.py

javac : 
	javac -d reference-classes -sourcepath java java/org/joellercoaster/*.java

test :
	./file_test.py

