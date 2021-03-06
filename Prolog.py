from game import Game
import copy

""" Prolog built-ins """

def var(term):
    return (term[0].isupper() or term[0] == '_')

def nonvar(term):
    return not var(term)

def compound(term):
    return '(' in term

def atom(term):
    return not compound(term) and not var(term)

def parse_expression(expression, aliases):
    # TODO: more operators, */, +- equality etc
    # TODO: handle brackets given
    for operator in ['*','/','+','-']:
        if operator in expression:
            left, op, right = expression.partition(operator)
            leftparse = parse_expression(left, aliases)
            rightparse = parse_expression(right, aliases)
            if type(leftparse) == str and type(rightparse) == str:
                if leftparse.isdigit() and rightparse.isdigit():
                    return str(eval(leftparse + op + rightparse))
            return leftparse, op, rightparse, 
    if var(expression) and expression in aliases:
        if aliases[expression].isdigit():
            return aliases[expression]
        else:
            # can't do arithmetics with nondigits! 
            # TODO: define proper error, handle floats (with .)
            raise Exception
    return expression

def univ(term):
    if atom(term):
        return [term]
    i = term.find('(')
    functor, args = term[:i], term[i+1:-1]
    return [functor] + args.split(',')

def unification_All(args1, args2, aliases):

    newaliases = copy.deepcopy(aliases)

    for arg1, arg2 in zip(args1, args2):
        unifies, al = unification(arg1, arg2, aliases)
        #print arg1, arg2, unifies, al
        if not unifies:
            return False, {}
        for k,v in al.items():
            if k in newaliases and not newaliases[k] == v:
                return False, {}
            newaliases[k] = v

    return True, newaliases

# TODO: check conflicts in aliases, do occurence checks!
def unification(term1, term2, aliases):

    # Two identical atoms

    if term1 == term2:  
        return True, aliases

    # Uninstantiated Var can be unified with atom, term or other uninstantiated var
    elif var(term1):
        if not term1 in aliases:
            if compound(term2) or atom(term2) or (var(term2) and not term2 in aliases):
                aliases[term1] = term2
                return True, aliases
        elif aliases[term1] == term2:
            return True, aliases

    elif var(term2): 
        if not term2 in aliases:
            aliases[term2] = term1
            return True, aliases
        elif aliases[term2] == term1:
            return True, aliases


    # Recursive: term with term if functor and arity are identical, and args can be unified

    else:
        decomp1 = univ(term1)
        functor1, args1 = decomp1[0], decomp1[1:]
        decomp2 = univ(term2)
        functor2, args2 = decomp2[0], decomp2[1:]
        if functor1 == functor2 and len(args1) == len(args2):
            return unification_All(args1, args2, aliases)

    return False, {}

""" End built-ins """

class Prolog(Game):

    def play(self):

        # https://www.csupomona.edu/~jrfisher/www/prolog_tutorial/3_1.html
        self.memory = { ('p',1) : [(['a'],[]), (['X'],['q(X)','r(X)']), (['X'],['u(X)'])], 
                        ('q',1) : [(['X'],['s(X)'])],
                        ('r',1) : [(['a'],[]), (['b'],[])],
                        ('s',1) : [(['a'],[]), (['b'],[]), (['c'],[])],
                        ('u',1):[(['d'],[])]}
        #self.builtin = [('var', 1), ('nonvar', 1), ('compound', 1), ('atom', 1), ('univ', 1)]

        done = False

        while not done:
            self.say('?-')
            
            inp = self.input()

            # TODO: Check validity of input

            if inp == "quit":
                done = True
                break

            if not inp[-1] == '.':
                self.say('Don\'t forget that period!')
                continue

            # TODO: Check validity!
            if inp.startswith("assert("):
                inp = inp[7:-2]
                if ":-" in inp:
                    [head, body] = inp.split(":-")
                    decomp1 = univ(head)
                    functor, args = decomp1[0], decomp1[1:]
                    rules = body.split(',')
                    if (functor, len(args)) in self.memory:
                        self.memory[(functor, len(args))] = self.memory[(functor, len(args))] + [(args,rules)]
                    else:
                        self.memory[(functor, len(args))] = [(args, rules)]
                else:
                    decomp = univ(inp)
                    functor, args = decomp[0], decomp[1:]
                    if (functor, len(args)) in self.memory:
                        self.memory[(functor, len(args))] = self.memory[(functor, len(args))] + [(args,[])]
                    else:
                        self.memory[(functor, len(args))] = [(args,[])]
                continue

            if inp.startswith("listing("):
                inp = inp[8:-2]
                functor, arity = inp.split('/')
                if (functor, int(arity)) in self.memory:
                    for head, rule in self.memory[(functor, int(arity))]:
                        print functor, '(', head[0],
                        for c in head[1:]:
                            print ',', c,
                        if rule:
                            print ') :- ',
                            for r in rule:
                                print r,
                            print ''
                        else:
                            print ').'
                continue

            # Handle input : functor ( comma-separated args )
            # TODO: arity/0

            stack = [([inp[:-1]], {})]

            while stack:

                print stack
                terms, aliases = stack.pop(0)
                print terms, aliases
                if not terms:
                    for k,v in aliases.items():
                        self.say(k + ' = ' + v)
                    self.say('True.')
                    # TODO: wait for ;
                    continue
                term = terms.pop(0)
                print term

                newstack = []

                if '=' in term:
                    [termleft, termright] = term.split('=')
                    #print termleft, termright
                    unifies, al = unification_All([termleft], [termright], aliases)
                    if unifies:
                        newaliases = copy.deepcopy(aliases)
                        for k,v in al.items():
                            if k in newaliases:
                                # TODO: clash
                                continue
                            else:
                                newaliases[k] = v
                        stack.insert(0, (terms, newaliases))

                elif ' is ' in term:

                    # TODOs:
                    # 2 is 3 -> True ><
                    

                    # Assume: var is expression
                    [var, expression] = term.split(' is ')
                    expression = parse_expression(expression, aliases)
                    #print expression
                    if var in aliases:
                        if aliases[var] == expression:
                            stack = [(terms, aliases)] + stack
                        else:
                            # TODO: unification of arithmetic expressions
                            unifies, al = unification(var, expression, aliases)
                            if unifies:
                                print "TODO"
                    else:
                        aliases[var] = expression
                        stack = [(terms, aliases)] + stack

                elif compound(term):

                    decomp = univ(term)
                    functor, args = decomp[0], decomp[1:]

                    if not (functor, len(args)) in self.memory:
                        continue
                    
                    for memargs in self.memory[(functor, len(args))]:
                        newterms = terms[:]
                        newaliases = copy.deepcopy(aliases)
                        unifies, al = unification_All(args, memargs[0], newaliases)
                        #print unifies, memargs[0], newaliases
                        if unifies:
                            for k,v in al.items():
                                if k in newaliases:
                                    # TODO: clash
                                    continue
                                else:
                                    newaliases[k] = v
                        else:
                            continue
                        newterms = memargs[1] + newterms
                        newstack.append((newterms, newaliases))
                    stack = newstack + stack
                else:
                    self.say('TODO')

            self.say('False.')

            # Should print: X = _G182, Y = b, Z = _G182
            #print unification_All(['X','f(Y)','a'], ['Z', 'f(b)', 'a'], {})
                        