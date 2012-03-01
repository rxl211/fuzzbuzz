#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from reg import registration

class NoExampleException(Exception):
    pass

@registration.register(
  {'example_list':'examples'},
  'Mutates the AST of the given example files s.t. conditions hold')
def mutation_fuzzer(rlexer, grammar, example_list=None):

    if not example_list:
        raise NoExampleException

    def generate_examples_ast(parser):
        """Generates an AST for each example provided in `example_list`.
        This AST is parsed according to the grammar in `grammar`.
        On completion, this function returns a list of ASTs, corresponding
        to the examples provided.

        Arguments:
        - `parser`: The parser from which the ASTs will be generated from
        """
        ast_list = list()

        for example in example_list:
            ast_list.append(generate_ast(example, parser))

        return ast_list

    def generate_ast(example, parser):
        """Generates and returns an AST for the provided `example`
        AST generated according to the provided grammar
        On completion, returns an AST object.

        Arguments:
        - `example`: the text to be parsed into an AST
        - `parser`:  the parser from which the ASTs will be generated from
        """
        pass

    def generate_parser(grammar_start):
        """Generate a parser for our `example_list` based on the grammar in
        `grammar`. This is probably going to be very hacky.
        On completion this function returns a `parser` object which can be
        used to generate ASTs for our examples.

        Arguments:
        - `grammar_start`: The start symbol for the grammar we are to generate
        a parser for
        """
        pass

    def mutate(ast):
        """Mutate a singular AST and return the resultant AST

        Arguments:
        - `ast`: the AST which we will mutate
        """
        pass


    def mutate_all(ast_list):
        """Takes in a list of AST and mutates them, returning a list of each
        AST in mutated form.

        Arguments:
        - `ast_list`: a list of ASTs to be mutated. See frontent/ast.py
        """
        mutated_list = list()
        for ast in ast_list:
            mutated_list.append(mutate(ast))
        return mutated_list


    parser = generate_parser(grammar.start)
    ast_list = generate_examples_ast(parser)
    mutated_asts = mutate_all(ast_list)
    return mutated_asts

