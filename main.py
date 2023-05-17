from grammar import Grammar

grammar1 = Grammar.str_to_grammar(
  '''
  S -> AB
  A -> 0
  B -> AB
  B -> 1
  '''
)

print(grammar1)
print(grammar1.is_cnf())