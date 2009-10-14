CLASS_DIR=classes

ANTLR_HOME=`cygpath -w /c/DevTools/antlr-3.1.3/lib`
JUNIT_HOME=`cygpath -w /c/DevTools/apache-ant-1.7.1/lib`

ANTLR=java -cp $(ANTLR_HOME)/antlr-3.1.3.jar org.antlr.Tool

ANTLR_DIR=antlr
ANTLR_OPTS=-o .

JUNIT_JAR = $(JUNIT_HOME)/junit.jar

JAVAC_OPTS=-d $(CLASS_DIR) -cp $(CLASS_DIR)\;$(JUNIT_JAR)

clean : 
	rm -rf *.pyc classes/org/ reference-classes/* *.tokens *Lexer.py *Parser.py

lexer : $(ANTLR_DIR)/PorkLexer.g
	$(ANTLR) $(ANTLR_OPTS) $(ANTLR_DIR)/PorkLexer.g

parser : lexer $(ANTLR_DIR)/Pork.g
	$(ANTLR) $(ANTLR_OPTS) $(ANTLR_DIR)/Pork.g

pork :
	cat prk/*.prk | python Pork.py --rule=porkfile

tests : pork
	javac $(JAVAC_OPTS) java/org/joellercoaster/pork/*.java java/org/joellercoaster/pork/test/JUnit.java

test : tests
	java -cp $(CLASS_DIR)\;$(JUNIT_JAR) org.joellercoaster.pork.test.JUnit

