import lsp
import codecs

TESTING_FILE = './testing.lsp'

PROGRAM_STRING = None
with codecs.open(TESTING_FILE, 'r', 'utf-8') as file:
    PROGRAM_STRING = file.read()  

stream = lsp.lexing.lex(PROGRAM_STRING, TESTING_FILE)

print("\n\n=== Token Stream ===\n")
print(stream)  


ast = lsp.parsing.parse(stream)

print("\n\n=== Abstract Syntax Tree ===\n")
print(ast)  

expanded = lsp.parsing.preprocess(ast)

print("\n\n=== Macro Expanded ===\n")
print(expanded)
