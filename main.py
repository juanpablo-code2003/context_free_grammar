from grammar import Grammar

grammar1 = Grammar.str_to_grammar(
  '''
  S -> ABC
  A -> 0A1
  A -> ''
  B -> 1B
  B -> 1
  C -> 1C0
  C -> ''
  ''', 'S'
)

print(grammar1)
print(grammar1.is_cnf())
print(grammar1.convert_to_cnf())