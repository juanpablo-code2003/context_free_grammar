import re

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Grammar:
  def __init__(self) -> None:
    self.alphabet = set()
    self.non_terminals = set()
    self.initial_terminal = ''
    self.rules = dict()
    
  def __str__(self) -> str:
    string = 'Initial: ' + self.initial_terminal + '\n'
    for left, right in self.rules.items():
      string += left + ' -> ' + ' | '.join(right) + '\n'
      
    return string
  
  def add_rule(self, left, right):
    self.non_terminals.add(left)
        
    for r in right:
      if re.fullmatch('[a-z0-9]', r):
        self.alphabet.add(r)
    
    if not left in self.rules:
      self.rules[left] = list()
      
    self.rules[left].append(right)
  
  def is_cnf(self):
    for left, right in self.rules.items():
      if "''" in right and left != 'S':
        return False
      for r in right:
        if not re.fullmatch('[a-z0-9]|([A-Z]){2}|\'\'', r):
          return False
      
    return True
  
  def get_new_non_terminal(self):
    for letter in LETTERS:
      if letter not in self.non_terminals: 
        print('+ ' + letter)
        return letter
      
    return None
  
  def get_rules_one_non_terminal(self, non_terminal: str):
    return self.rules[non_terminal]
  
  def convert_to_cnf(self):
    new_grammar = Grammar()
    if self.is_cnf():
      return self
    
    new_grammar.alphabet = self.alphabet
    new_grammar.initial_terminal = self.initial_terminal
    new_grammar.non_terminals = self.non_terminals
    
    new_non_terminal = new_grammar.get_new_non_terminal()
    new_grammar.add_rule(new_non_terminal, self.initial_terminal)
    new_grammar.initial_terminal = new_non_terminal
    
    
    # elimina reglas con terminales junto a no terminales
    for left, right in self.rules.copy().items():
      for r in right:
        if re.fullmatch('([a-z0-9])+|([A-Z])+|\'\'', r):
          new_grammar.add_rule(left, r)
        else:
          new_right_rule = ''
          for symbol in r:
            if symbol in self.alphabet:
              new_non_terminal = new_grammar.get_new_non_terminal()
              new_grammar.add_rule(new_non_terminal, symbol)
              new_right_rule += new_non_terminal
            else:
              new_right_rule += symbol
              
          new_grammar.add_rule(left, new_right_rule)
        
    # Elimina las reglas con más de dos no terminales
    for left, right in new_grammar.rules.copy().items():
      for r in right:
        if re.fullmatch('[A-Z]{3,}', r):
          if len(r) > 2:
            j = 0
            queue = r
            
            new_non_terminal = new_grammar.get_new_non_terminal()
            new_grammar.rules[left].remove(r)
            new_grammar.add_rule(left, queue[0] + new_non_terminal)
            j += 1
            queue = queue[j:]
            
            while j < len(queue) - 1:
              past_non_terminal = new_non_terminal
              new_grammar.non_terminals.add(past_non_terminal)
              new_non_terminal = new_grammar.get_new_non_terminal()
              new_grammar.add_rule(past_non_terminal, queue[0] + new_non_terminal)
              j += 1
              queue = queue[j:]
              
            new_grammar.add_rule(new_non_terminal, queue)
            
          
    # Elimina los epsilon (a excepcion del inicial)
    epsilon_rules_non_terminals = list()
    for left, right in new_grammar.rules.copy().items():
      for r in right:
        if r == "''" and left != new_grammar.initial_terminal:
          epsilon_rules_non_terminals.append(left)
          new_grammar.rules[left].remove(r)
          break
        
    for left, right in new_grammar.rules.copy().items():
      count_non_terminal = 0
      for r in right:
        for symbol in r:
          if symbol in epsilon_rules_non_terminals:
            if len(r) == 2:
              if count_non_terminal == 0:
                new_grammar.add_rule(left, r[1])
              else:
                new_grammar.add_rule(left, r[0])
          count_non_terminal += 1
      
      
    # Elimina las reglas con un solo no terminal
    for left, right in new_grammar.rules.items():
      for r in right:
        if re.fullmatch('[A-Z]{1}', r):
          new_grammar.rules[left].extend(new_grammar.rules[r])
          new_grammar.rules[left].remove(r)
          
    new_grammar.rules.pop(new_grammar.initial_terminal)
    new_grammar.initial_terminal = self.initial_terminal
      
    return new_grammar
  
  @classmethod
  def str_to_grammar(cls, grammar: str, initial: str):
    grammar_obj = Grammar()
    rules = grammar.strip().splitlines()
    for rule in rules:
      if re.fullmatch('( )*[A-Z]( )*->( )*(\'\'|[a-zA-Z0-9]+)( )*', rule):
        left, right = rule.split('->')
        left = left.strip()
        right = right.strip().split('|')
        for r in right:
          grammar_obj.add_rule(left, r)
      else:
        print('Error: '+rule+' no es una regla valida')
        return None
      
    grammar_obj.initial_terminal = initial
        
    return grammar_obj