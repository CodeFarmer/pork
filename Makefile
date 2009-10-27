CLASS_DIR=classes

ANTLR_HOME=$(HOME)/antlr-3.1.3/lib
JUNIT_HOME=$(HOME)/junit3.8.2

ANTLR=java -cp $(ANTLR_HOME)/antlr-3.1.3.jar org.antlr.Tool

ANTLR_DIR=antlr
ANTLR_OPTS=-fo "$(PWD)"

JUNIT_JAR = $(JUNIT_HOME)/junit.jar

JAVAC_OPTS=-d $(CLASS_DIR) -cp $(CLASS_DIR):$(JUNIT_JAR)

clean: 
	rm -rf *.pyc classes/org/ reference-classes/* *.tokens *Lexer.py Pork.py

PorkLexer.py: $(ANTLR_DIR)/PorkLexer.g
	$(ANTLR) $(ANTLR_OPTS) $(ANTLR_DIR)/PorkLexer.g

Pork.py: $(ANTLR_DIR)/Pork.g PorkLexer.py
	$(ANTLR) $(ANTLR_OPTS) $(ANTLR_DIR)/Pork.g

parser: Pork.py
	
pork:
	python pjc.py prk/*.prk

tests: pork
	javac $(JAVAC_OPTS) test/java/org/joellercoaster/pork/*.java test/java/org/joellercoaster/pork/test/JUnit.java

junit-tests: tests
	java -cp $(CLASS_DIR):$(JUNIT_JAR) org.joellercoaster.pork.test.JUnit

pyunit-tests:

test: parser pyunit-tests junit-tests
	for i in test/python/*.py ; do PYTHONPATH="$(PWD)" python $$i ; done


