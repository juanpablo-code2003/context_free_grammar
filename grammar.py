import re

class Grammar:
  def __init__(self) -> None:
    self.alphabet = set()
    self.non_terminals = set()
    self.initial_terminal = ''
    self.rules = list()
    
  def __str__(self) -> str:
    return self.rules.__str__()
  
  def is_cnf(self):
    for rule in self.rules:
      if rule[1] == "''" and rule[0] != 'S':
        return False
      if not re.fullmatch('[a-z0-9]|([A-Z]){2}|\'\'', rule[1]):
        return False
      
    return True
  
  def convert_to_cnf(cls, grammar):
    return Grammar()
  
  @classmethod
  def str_to_grammar(cls, grammar: str):
    # Por defecto, S es el no terminal inicial
    grammar_obj = Grammar()
    rules = grammar.strip().splitlines()
    for rule in rules:
      if re.fullmatch('( )*[A-Z]( )*->( )*(\'\'|[a-zA-Z0-9]+)( )*', rule):
        left, right = rule.split('->')
        left = left.strip()
        right = right.strip()
        grammar_obj.non_terminals.add(left)
        
        for r in right:
          if re.fullmatch('[a-z0-9]', r):
            grammar_obj.alphabet.add(r)
        
        grammar_obj.rules.append((left, right))
      else:
        print(rule)
        return None
        
    return grammar_obj