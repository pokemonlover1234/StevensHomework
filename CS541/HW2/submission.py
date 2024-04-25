import collections, sys, os
from logic import *

############################################################
# Problem 1: propositional logic
# Convert each of the following natural language sentences into a propositional
# logic formula.  See rainWet() in examples.py for a relevant example.
# sentence: If I have a deadline tomorrow and I'm watching TV, then I'm not being productive.
def formula1a():
    # Predicates to use:
    tomorrow = Atom('Tomorrow')               # whether I have a deadline tomorrow
    TV = Atom('TV')                 # whether I'm watching TV
    productive = Atom('Productive')               # whether I'm being productive
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Implies(And(tomorrow, TV), Not(productive))
    # END_YOUR_CODE

# sentence: Either I'll go to the gym or go for a run (but not both).
def formula1b():
    # Predicates to use:
    gym = Atom('Gym')     # whether I'll go to the gym
    run = Atom('Run') # whether I'll go for a run
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Or(And(gym, Not(run)), And(Not(gym), run))
    # END_YOUR_CODE

# sentence: The store is open if and only if the sign says "open" and the lights are on.
def formula1c():
    # Predicates to use:
    store = Atom('Store')              # whether the sign says it's open
    O = Atom('Open')                # whether the store is open
    lights = Atom('Lights')  # whether the lights are on
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return Equiv(O, And(store, lights))
    # END_YOUR_CODE

############################################################
# Problem 2: first-order logic
# sentence: some people are students, some people are teacher. 
# There exists at least 1 student and 1 teacher, any person must either be a student or a teacher. 
# only student can learn, and only teacher can teach. Every student must have at least one teacher
def formula2a():
    # Predicates to use:
    def Student(x): return Atom('Student', x)
    def Teacher(x): return Atom('Teacher', x)
    def Teaches(x, y): return Atom('Teaches', x, y)
    # BEGIN_YOUR_CODE
    x = '$x'
    y = '$y'
    return AndList([
        Forall(x, Or(And(Student(x), Not(Teacher(x))), And(Not(Student(x)), Teacher(x)))),
        And(Exists(x, Student(x)), Exists(y, Teacher(y))),
        Forall(x, Forall(y, AndList([Implies(And(Student(x), Teacher(y)), Not(Teaches(x, y))),
                                     Implies(And(Student(x), Student(y)), Not(Teaches(x, y))),
                                     Implies(And(Teacher(x), Teacher(y)), Not(Teaches(x, y)))]))),
        Forall(x, Implies(Student(x), Exists(y, And(Teacher(y), Teaches(y, x)))))
    ])

# sentence: Teacher can also learn from teacher, but student cannot teach
def formula2b():
    # Predicates to use:
    def Student(x): return Atom('Student', x)
    def Teacher(x): return Atom('Teacher', x)
    def Teaches(x, y): return Atom('Teaches', x, y)
    # BEGIN_YOUR_CODE
    x = '$x'
    y = '$y'
    return AndList([
        Forall(x, Or(And(Student(x), Not(Teacher(x))), And(Not(Student(x)), Teacher(x)))),
        And(Exists(x, Student(x)), Exists(y, Teacher(y))),
        Forall(x, Forall(y, Implies(Student(x), Not(Teaches(x, y))))),
        Forall(x, Implies(Student(x), Exists(y, And(Teacher(y), Teaches(y, x)))))
    ])


############################################################
# Problem 3: Liar puzzle
# Facts:
# • Adam says: "My shirt is not blue."
# • Levi says: "Adam’s shirt is red."
# • John says: "Levi’s shirt is not blue."
# • Luke says: "John’s shirt is blue.
# • You know that exactly one person is telling the truth 
# • and exactly one person is wearing a red shirt.
# # Query: Who is telling the truth?
# This function returns a list of 6 formulas corresponding to each of the above facts.
# Hint: You might want to use the Equals predicate, defined in logic.py.  
# This predicate is used to assert that two objects are the same.
# In particular, Equals(x,x) = True and Equals(x,y) = False iff x is not equal to y.

def liar():
    def WearsRed(x): return Atom('WearsRed', x)
    def TellTruth(x): return Atom('TellTruth', x)
    luke = Constant('luke')
    john = Constant('john')
    levi = Constant('levi')
    adam = Constant('adam')
    x = '$x'
    y = '$y'
    formulas = []
    # We provide the formula for fact 0 here.
    formulas.append(Equiv(TellTruth(adam), WearsRed(adam)))
    # You should add 5 formulas, one for each of facts 1-5.
    # BEGIN_YOUR_CODE 
    formulas.append(Equiv(TellTruth(levi), WearsRed(adam)))
    formulas.append(Equiv(TellTruth(john), WearsRed(levi)))
    formulas.append(Equiv(TellTruth(luke), Not(WearsRed(john))))
    formulas.append(And(Exists(x, TellTruth(x)), Forall(x, Implies(TellTruth(x), 
                                      Forall(y, Implies(Not(Equals(x, y)),
                                                        Not(TellTruth(y))))))))
    formulas.append(And(Exists(x, WearsRed(x)), Forall(x, Implies(WearsRed(x), 
                                      Forall(y, Implies(Not(Equals(x, y)),
                                                        Not(WearsRed(y))))))))
    # END_YOUR_CODE
    query = TellTruth('$x')
    return (formulas, query)

