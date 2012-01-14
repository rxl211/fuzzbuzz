#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

## Should contain the implementation of the main fuzzing algorithm.

from random import seed, choice

from frontend import parser
from models.nonterminal import NonTerminal

def init():
    seed()

def fuzz(grammar):

    def fuzz(start):
        stack = list()
        stack.append(start)
        while stack:
            nonterm = stack.pop()
            rule = choice(nonterm.rules)
            for sym, cnt in rule.pattern:
                if isinstance(sym, NonTerminal):
                    stack.append(sym)
                else:
                    yield sym
                    

    return list(fuzz(grammar.start))

def main():
    init()
    tree, grammar = parser.parse('''
    Stmts -> Stmts Stmt
                with Action {
                  if (Stmt.decl is not None) {
                    Stmts{1}.names = Stmts{2}.names | { stmt.decl }
                  }
                  else {
                    Stmts{1}.names = Stmts{2}.names
                  }
                }
                with Condition {
                  (Stmt.uses is not None && Stmt.uses in Stmts{2}.names) ||
                  (Stmt.decl is not None && Stmt.decl not in Stmts{2}.names)
                }
              | Stmt
                with Action {
                  Stmts{1}.names = { stmt.decl }
                }
                with Condition {
                  Stmt.uses is None
                }
              ;

    Stmt -> VAR NAME EQUAL NUMBER
            with Action {
              Stmt.decl = NAME.value
              Stmt.uses = None
            }
          | PRINT NAME
            with Action {
              Stmt.decl = None
              Stmt.uses = NAME.value
            }
          ;
    ''')
    #print repr(tree)
    #print grammar
    print fuzz(grammar)

if __name__ =='__main__':
    main()
