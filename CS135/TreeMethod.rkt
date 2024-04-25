;;Rules of Inference (Test Cases for valid)

;;Modus ponens: (q p (IMP p q))
;;Modus tollens: ((NOT p) (NOT q) (IMP p q))
;;Addition: ((OR p q) p)
;;Simplification: (p (AND p q))
;;Conjunction: ((AND p q) p q)
;;Hypothetical syllogism: ((IMP p r) (IMP p q) (IMP q r))
;;Disjunctive syllogism: (q (OR p q) (NOT p))
;;Resolution: ((OR q r) (OR p q) (OR (NOT p) r))


;;Monster valid test case

;;((NOT E) (IMP E OP) (IMP E ON) (IMP E B) (IMP P (IMP K (IMP (NOT Z) (NOT B)))) (IMP (NOT P) (NOT OP)) (IMP ON (IMP X K)) (IMP Z (NOT X)) X)

;;Monster counterexample test case
;;((IMP (NOT A) (IMP D B)) (IMP A (IMP B C)) (IMP (NOT C) (AND (NOT B) D)) (IMP D (OR A (NOT C))))


#lang racket
;;Name: Aidan Fischer
;;Pledge: I pledge my honor that I have abided by the Stevens Honor System

;;Use the tree method to determine validity of a set of hypothesis and a conclusion
;;The methods in this file use OR to represent or, AND to represent and, NOT to represent not and IMP to represent implications
;;propositions are in the form (operation leftside [rightside])
;;This also means that propositions that have more than 2 terms (AVBVC) should be written in the form (operation A (operation B C)) or (operation (operation A B) C).

;;While technically a prop typed out using the list function would be valid, the way user input is processed it doesn't actually work, so user input is expected to be in symbol
;;form rather than list function form (i.e. use (IMP A B) rather than (list "IMP" "A" "B")

;;Examples:
;;(OR A B)
;;(AND (OR A B) (NOT C))
;;(AND (AND A B) C)

;;Base definitions for operations to simplify using them in methods
(define NOT "NOT")
(define AND "AND")
(define OR "OR")
(define IMP "IMP")

;;Get type of proposition, regardless of method used to define the list
;;Type signature (prop-type list) -> string
(define (prop-type prop) (if (symbol? (car prop)) (symbol->string (car prop)) (car prop)))

;;Check if a prop is a certain proposition

;;The proposition should be valid as a certain type whether the type is a symbol or the identifier
;;That is, the prop should be valid as an IMP whether the prop is defined as (list IMP "A" "B")
;;or as '(IMP A B)

;;Be careful not to confuse this method with prop-type, which gets the type of the proposition, while
;;this one checks if a given proposition is a certain type.

;;Type signature (prop-type? lst string) -> bool
(define (prop-type? prop type) (equal? type (prop-type prop)))

;;Recursively check if a prop is a valid proposition, regardless of type
;;Attach an exception handler to return false should any error occur
;;(such as a contract violation in prop-type? when given i.e. an empty list within the prop
;;which would mean the proposition was invalid)
;;This makes it slightly easier to type validate since it means the function doesn't have to check
;;manually for edge cases that would cause an error, since those errors are caught automatically.
;;A valid proposition shouldn't cause an error, and an error-causing input shouldn't be valid.

;;Note that the way prop? is defined allows for mixed (list items) and '(items) definitions within the
;;nested propositions. This means (list AND '(OR A B) (list OR "A" "C")) is a valid definition of
;;a proposition.

;;Type signature (prop? list) -> bool 
(define (prop? prop) (with-handlers ([exn:fail? (lambda (exn) #f)])
                       ;;Check the length of the proposition list. Should only be 2 if the type is NOT, otherwise 3.
                      (if (eq? (length prop) (if (prop-type? prop NOT) 2 3))
                         ;;Should have a valid operation and have a valid left and right side (UNLESS IT IS A NOT, THEN ONLY ONE SIDE)
                         (and (or (prop-type? prop NOT) (prop-type? prop AND) (prop-type? prop OR) (prop-type? prop IMP))
                              (cond
                                ;;If the proposition type is a NOT, then only one input to check
                                [(prop-type? prop NOT) (if (list? (cadr prop)) (prop? (cadr prop)) (or (symbol? (cadr prop)) (string? (cadr prop))))]
                                ;;If both the left and right sides are propositions, check if both are also valid.
                                [
                                 (and (list? (cadr prop)) (list? (caddr prop)))
                                 (and (prop? (cadr prop)) (prop? (caddr prop)))
                                 ]
                                ;;If one or the other are a prop and the other is not, check the prop and see if the non-prop is a symbol or a string.
                                [
                                 (and (list? (cadr prop)) (not (list? (caddr prop))))
                                 (and (prop? (cadr prop)) (or (symbol? (caddr prop)) (string? (caddr prop))))
                                 ]
                                [
                                 (and (list? (caddr prop)) (not (list? (cadr prop))))
                                 (and (prop? (caddr prop)) (or (symbol? (cadr prop)) (string? (cadr prop))))
                                 ]
                                ;;Otherwise, check if both are a symbol or a string
                                [else (and (or (symbol? (cadr prop)) (string? (cadr prop))) (or (symbol? (caddr prop)) (string? (caddr prop))))]
                                )) #f)))

;;prop-top? is a less-strict version of prop? for when we expect a valid prop all the way down but we need to know if a certain level is a prop or a symbol or string.
;;This is non-recursive and simply checks the top level. Since we expect a valid prop, if it is a list we can already say it is a prop but just for sanity check it
;;anyways, plus using prop-top? makes it clearer what we are checking for, rather than just checking if it is a list. IMO makes the code slightly easier to read.

;;Type signature: (prop-top? symbol/string/list) -> bool
(define (prop-top? item) (if (list? item) (if (or (eq? (length item) 2) (eq? (length item) 3)) (or (prop-type? item NOT) (prop-type? item OR) (prop-type? item AND) (prop-type? item IMP)) #f) #f) )

;;The following functions manipulate and simplify a given proposition
;;Note the following functions expect a valid proposition.
;;As such, I will start treating prop as a type in type signatures

;;Check if a proposition can be reduced via double negation

;;Type signature: (dblnegatable? prop) -> bool

(define (dblnegatable? prop) (if (prop? prop) (if (prop-type? prop NOT) (if (prop-top? (cadr prop)) (if (prop-type? (cadr prop) NOT) #t #f) #f) #f) #f))

;;Reduce a double negation

;;Type signature: (dblnegate prop) -> prop

(define (dblnegate prop) (if (dblnegatable? prop) (cadr (cadr prop))
                             (raise-argument-error 'dblnegate "Double Negation" prop)))

;;Convert implications into OR form
;;Take a proposition that is an implication and convert it to or form.

;;Only used for propositions of form (IMP left right)
;;If not an implication, return a violation.

;;Check whether the operation in the list is an implication, otherwise raise a contract violation

;;Type signature: (imp->or prop) -> prop
(define (imp->or prop) (if (prop-type? prop IMP) (list OR (list NOT (cadr prop)) (caddr prop))
                          (raise-argument-error 'imp->or "Implication" prop)))

;;Check if De Morgan's can be applied to a given proposition

;;Type signature: (demorganable? prop) -> bool
(define (demorganable? prop) (if (prop? prop) (if (prop-type? prop NOT) (let ([subprop (cadr prop)]) (if (prop-top? subprop) (if (or (prop-type? subprop AND) (prop-type? subprop OR)) #t #f) #f)) #f) #f))

;;Apply De Morgan's Law to a proposition
;;after checking De Morgan's applies

;;Type signature: (demorgan prop) -> prop
(define (demorgan prop) (if (demorganable? prop) (list (if (prop-type? (cadr prop) AND) OR AND) (list NOT (cadr (cadr prop))) (list NOT (caddr (cadr prop))))
                            (raise-argument-error 'demorgan "DeMorganable Proposition" prop)))

;;This section creates recursive versions of the manipulation functions to do full manipulation throughout the entire given proposition.

;;Recursively go through and apply double negation where applicable
;;If double negation at any level result in no proposition but just a symbol or string,
;;simply return that symbol or string. Note we can assume that it is either a symbol or
;;string or prop since we expect a valid prop in this function.

;;Type signature: (dblnegateall prop) -> prop or symbol
                                  ;;If this level is a not and there is a subprop, check if we can apply double negation.
(define (dblnegateall prop) (if (not (or (symbol? prop) (string? prop))) (cond [(prop-type? prop NOT)
                                  ;;If this level is a not, check if you can apply double negation. If so,
                                  ;;apply it and continue, else if it's a base case return, else continue down the proposition.
                                   (if (prop-top? (cadr prop)) (if (dblnegatable? prop) (dblnegateall (dblnegate prop)) (list NOT (dblnegateall (cadr prop)))) prop)]
                                  ;;Note that here the top level of proposition we are at is definition not a NOT, so we definitely CANNOT apply double negation at this layer.
                                  ;;So, start with other cases where there are subpropositions we can go through or not.
                                  [(and (prop-top? (cadr prop)) (prop-top? (caddr prop)))
                                   (list (prop-type prop) (dblnegateall (cadr prop)) (dblnegateall (caddr prop)))]
                                  [(and (prop-top? (cadr prop)) (not (prop-top? (caddr prop))))
                                   (list (prop-type prop) (dblnegateall (cadr prop)) (caddr prop))]
                                  [(and (prop-top? (caddr prop)) (not (prop-top? (cadr prop))))
                                   (list (prop-type prop) (cadr prop) (dblnegateall (caddr prop)))]
                                  ;;Finally, if neither are props we are at the other base case.
                                  [else prop]
                                  ) prop))

;;Go through the entire proposition and apply De Morgans wherever possible.
;;Also double negate at each step

;;Type signature: (demorganall prop) -> prop

(define (demorganall p) (let ([prop (if (dblnegatable? p) (dblnegate p) p)])(cond
                                  [(or (symbol? prop) (string? prop)) prop]
                                  [(prop-type? prop NOT)
                                  ;;This includes a recursive case and a base case in one.
                                  ;;If it is demorganable, apply De Morgan's and continue,
                                  ;;else check if not holds a proposition as it's operand.
                                  ;;If so, continue, otherwise base case, so return prop.
                                  (if (prop-top? (cadr prop)) (if (demorganable? prop) (demorganall (demorgan prop)) (list NOT (demorganall (cadr prop)))) prop)]
                                  ;;Note that here the top level of proposition we are at is definition not a NOT, so we definitely CANNOT apply double negation at this layer.
                                  ;;So, start with other cases where there are subpropositions we can go through or not.
                                  [(and (prop-top? (cadr prop)) (prop-top? (caddr prop)))
                                   (list (prop-type prop) (demorganall (cadr prop)) (demorganall (caddr prop)))]
                                  [(and (prop-top? (cadr prop)) (not (prop-top? (caddr prop))))
                                   (list (prop-type prop) (demorganall (cadr prop)) (caddr prop))]
                                  [(and (prop-top? (caddr prop)) (not (prop-top? (cadr prop))))
                                   (list (prop-type prop) (cadr prop) (demorganall (caddr prop)))]
                                  ;;Finally, if neither are props we are at the other base case.
                                  [else prop]
                                 )))

;;Finally, a method for taking care of implications throughout the entire proposition.

;;Type signature: (implicateall prop) -> prop

(define (implicateall p) (let ([prop (if (dblnegatable? p) (dblnegate p) p)])(cond
                                  [(or (symbol? prop) (string? prop)) prop]
                                  [(prop-type? prop IMP)
                                  ;;If it's an implication, convert it and continue.
                                  (implicateall (imp->or prop))]
                                  ;;If it's a NOT, deal with the recursive and base cases.
                                  [(prop-type? prop NOT) (if (prop-top? (cadr prop)) (list NOT (implicateall (cadr prop))) prop)]                                
                                  ;;Note that here the top level of proposition we are at is definition not a NOT, so we definitely CANNOT apply double negation at this layer.
                                  ;;So, start with other cases where there are subpropositions we can go through or not.
                                  [(and (prop-top? (cadr prop)) (prop-top? (caddr prop)))
                                   (list (prop-type prop) (implicateall (cadr prop)) (implicateall (caddr prop)))]
                                  [(and (prop-top? (cadr prop)) (not (prop-top? (caddr prop))))
                                   (list (prop-type prop) (implicateall (cadr prop)) (caddr prop))]
                                  [(and (prop-top? (caddr prop)) (not (prop-top? (cadr prop))))
                                   (list (prop-type prop) (cadr prop) (implicateall (caddr prop)))]
                                  ;;Finally, if neither are props we are at the other base case.
                                  [else prop]
                                 )))

;;These functions are related to manipulations and actions for tree method

;;Full simplication and manipulation of a preposition:
;;Start by converting all implications then apply demorgans
;;These two functions deal with double negations at all steps.

;;Type signature: (simplify prop) -> prop

(define (simplify prop) (demorganall (implicateall prop)))

;;Given a list of pairs of variables and their boolean states,
;;Determine if a contradiction exists

;;Type signature: (contradiction? list) -> bool

(define (counterexample? pairs) (if (null? pairs) #t (let ([contradiction (list (caar pairs) (not (cadar pairs)))])
                                                      (if (list? (member contradiction pairs)) #f (counterexample? (cdr pairs))))))



;;Tree method time.
;;Check the input and do pre-processing on the propositions assuming they are valid.
;;Input list is of the form (conc hyp1 hyp2 hyp3)
;;The helper function does the work and prints out any contradictions if they exist.
;;If none exist the main function says so.

;;The first value in the list of props should be the conclusion, followed by the hypothesis
;;NOTE: THE CONCLUSION WILL ALREADY BE NEGATED BY THE TIME IT REACHES THIS FUNCTION.

;;Type signature (treemethod list) -> prints list or string
;;               (treemethodhelper list list set) -> bool
;;               (prop->assignments list list list prop) -> list
;;               (AND->assignments prop) -> list

(define (treemethod props) (let ([propositions (map (lambda (p) (if (prop? p) (simplify p) p)) props)]) (let ([assignments (filter-map (lambda (item) (if (or (symbol? item) (string? item)) (list (if (string? item) item (symbol->string item)) #t)
                            (if (prop? item) (if (and (prop-type? item NOT) (or (string? (cadr item)) (symbol? (cadr item)))) (list (if (string? (cadr item)) (cadr item) (symbol->string
                            (cadr item))) #f) #f) #f))) propositions)]) (let ([p (filter-map (lambda (proposition) (if (prop? proposition) (if (and (prop-type? proposition NOT)
                            (or (symbol? (cadr proposition)) (string? (cadr proposition)))) #f proposition) (if (or (symbol? proposition) (string? proposition))
                            #f (raise-argument-error 'treemethod "Valid Proposition" proposition)))) propositions)]) (treemethodhelper (cdr p) (list
                            (car p)) assignments)(print "")))))
;;It is time to traverse through the propositions and look for contradictions using the tree method.
(define (treemethodhelper hypotheses conclusion assignments) (cond [(null? hypotheses)
                                                                   (cond [(null? conclusion) (if (counterexample? assignments) (begin (print "Counterexample: ")(println assignments)#f) #t)]
                                                                         [else (prop->assignments hypotheses (cdr conclusion) assignments (car conclusion) #t)])]
                                                                   [else (prop->assignments (cdr hypotheses) conclusion assignments (car hypotheses) #f)]))

;;Take a prop from treemethodhelper and add it to the "tree" of recursive calls.
;;Also, base case is within treemethodhelper, since this recursive calls its parent
;;
;;This is by far the most complicated function in this project, but since a ton
;;of possible states have been made theoretically impossible by previous functions
;;(for example, because of demorganall we can assume that any nots will only have
;;a constant as an operand), we don't have to deal with those cases. This reduces
;;the number of conditions we need to account for. However, there are still a lot
;;and this function became very large, even though it is only meant to be a helper
;;function. I could split this up down into more helper functions but I feel the
;;cond conditionals do a good job of representing what state it is handling.
;;
;;This will also seperate each prop in a list of props into equivalent hypothesis
;;i.e.
;;A and (B or C)
;;is equivalent to
;;A
;;B or c

;;Type signature: (prop->assignments list list list prop bool) -> recursive call to treemethodhelper
;;                                                                       At this point, a "simplified" prop should be passed here.
;;                                                                       Meaning, any NOTS should only have symbols, not props, as
;;                                                                       the operand, and any top level nots (such as (NOT A) should've already been
;;                                                                       filtered out as a constant into the assignments list.
(define (prop->assignments hypothesis conclusion assignments prop isconc?) (cond [(prop-type? prop AND)
                                                                          (cond [(and (not (prop-top? (cadr prop))) (not (prop-top? (caddr prop))))
                                                                                 ;;"Base" case, neither are subprops so assume they are a variable.
                                                                                 ;;Add to assignments and bubble up.
                                                                                 (treemethodhelper hypothesis conclusion (remove-duplicates (append assignments (list 
                                                                                 (list (if (string? (cadr prop)) (cadr prop) (symbol->string (cadr prop))) #t)
                                                                                 (list (if (string? (caddr prop)) (caddr prop) (symbol->string (caddr prop))) #t)))))]
                                                                           ;;One or the other or both are subprops, deal with them.
                                                                                [(and (prop-top? (cadr prop)) (not (prop-top? (caddr prop))))
                                                                                 (if (prop-type? (cadr prop) NOT)
                                                                                 (treemethodhelper hypothesis conclusion (remove-duplicates (append assignments (list (list (if (string?
                                                                                 (cadadr prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) (list (if (string?
                                                                                 (caddr prop)) (caddr prop) (symbol->string (caddr prop))) #t))))) (treemethodhelper
                                                                                 (if isconc? hypothesis (cons (cadr prop) hypothesis)) (if isconc? (cons (cadr prop)
                                                                                 conclusion) conclusion) (remove-duplicates (cons (list (if (string? (caddr prop)) (caddr prop) (symbol->string
                                                                                 (caddr prop))) #t) assignments))))]
                                                                                 [(and (prop-top? (caddr prop)) (not (prop-top? (cadr prop))))
                                                                                 (if (prop-type? (caddr prop) NOT)
                                                                                 (treemethodhelper hypothesis conclusion (remove-duplicates (append assignments (list (list (if (string?
                                                                                 (cadr (caddr prop))) (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f) (list (if (string?
                                                                                 (cadr prop)) (cadr prop) (symbol->string (cadr prop))) #t))))) (treemethodhelper
                                                                                 (if isconc? hypothesis (cons (caddr prop) hypothesis)) (if isconc? (cons (caddr prop)
                                                                                 conclusion) conclusion) (remove-duplicates (cons (list (if (string? (cadr prop)) (cadr prop) (symbol->string
                                                                                 (cadr prop))) #t) assignments))))]
                                                                                 [(and (prop-top? (cadr prop)) (prop-top? (caddr prop)))
                                                                                  (cond [(and (not (prop-type? (cadr prop) NOT)) (not (prop-type? (caddr prop) NOT)))
                                                                                         (treemethodhelper (if isconc? hypothesis (append (list (cadr prop) (caddr prop)) hypothesis))
                                                                                         (if isconc? (append (list (cadr prop) (caddr prop)) conclusion) conclusion) assignments)]
                                                                                        [(and (prop-type? (cadr prop) NOT) (not (prop-type? (caddr prop) NOT)))
                                                                                         (treemethodhelper (if isconc? hypothesis (cons (caddr prop) hypothesis)) (if isconc?
                                                                                         (cons (caddr prop) conclusion) conclusion) (remove-duplicates (cons (list (if (string?
                                                                                         (cadadr prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) assignments)))]
                                                                                        [(and (prop-type? (caddr prop) NOT) (not (prop-type? (cadr prop) NOT)))
                                                                                         (treemethodhelper (if isconc? hypothesis (cons (cadr prop) hypothesis)) (if isconc?
                                                                                         (cons (cadr prop) conclusion) conclusion) (remove-duplicates (cons (list (if (string?
                                                                                         (cadr (caddr prop))) (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f)
                                                                                          assignments)))]
                                                                                        [(and (prop-type? (cadr prop) NOT) (prop-type? (caddr prop) NOT))
                                                                                         (treemethodhelper hypothesis conclusion (remove-duplicates (append (list (list (if (string? (cadadr
                                                                                         prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) (list (if (string? (cadr (caddr prop)))
                                                                                         (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f)) assignments)))])]
                                                                                )]
                                                                                 ;;Time to deal with or! Note that here instead of everything being in one call to treemethodhelper, there are
                                                                                 ;;two seperate calls. This represents the split that happens on ORs in the tree method.
                                                                                 [(prop-type? prop OR)
                                                                                 (cond [(and (not (prop-top? (cadr prop))) (not (prop-top? (caddr prop))))
                                                                                        (treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadr prop)) (cadr prop)
                                                                                        (symbol->string (cadr prop))) #t) assignments)))(treemethodhelper hypothesis conclusion (remove-duplicates
                                                                                        (cons (list (if (string? (caddr prop)) (cadr prop) (symbol->string (caddr prop))) #t) assignments)))]
                                                                                       [(and (prop-top? (cadr prop)) (not (prop-top? (caddr prop))))
                                                                                        (if (prop-type? (cadr prop) NOT) (begin (treemethodhelper hypothesis conclusion (remove-duplicates (cons
                                                                                        (list (if (string? (cadadr prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) assignments)))(treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (caddr prop))
                                                                                        (caddr prop) (symbol->string (caddr prop))) #t) assignments)))) (begin (treemethodhelper (if isconc? hypothesis (cons (cadr prop) hypothesis)) (if isconc? (cons (cadr prop) conclusion) conclusion)
                                                                                        assignments)(treemethodhelper hypothesis conclusion (remove-duplicates (cons (if (string? (caddr prop)) (caddr prop) (symbol->string (caddr prop))) assignments)))))]
                                                                                       [(and (prop-top? (caddr prop)) (not (prop-top? (cadr prop))))
                                                                                        (if (prop-type? (caddr prop) NOT) (begin (treemethodhelper hypothesis conclusion (remove-duplicates (cons
                                                                                        (list (if (string? (cadr (caddr prop))) (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f) assignments)))(treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadr prop))
                                                                                        (cadr prop) (symbol->string (cadr prop))) #t) assignments)))) (begin (treemethodhelper (if isconc? hypothesis (cons (caddr prop) hypothesis)) (if isconc? (cons (caddr prop) conclusion) conclusion)
                                                                                        assignments)(treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadr prop)) (cadr prop) (symbol->string (cadr prop))) #t) assignments)))))]
                                                                                       [(and (prop-top? (cadr prop)) (prop-top? (caddr prop)))
                                                                                        (cond [(and (not (prop-type? (cadr prop) NOT)) (not (prop-type? (caddr prop))))
                                                                                               (treemethodhelper (if isconc? hypothesis (cons (cadr prop) hypothesis)) (if isconc? (cons (cadr prop) conclusion) conclusion) assignments)
                                                                                               (treemethodhelper (if isconc? hypothesis (cons (caddr prop) hypothesis)) (if isconc? (cons (caddr prop) conclusion) conclusion) assignments)]
                                                                                              [(and (prop-type? (cadr prop) NOT) (not (prop-type? (caddr prop) NOT)))
                                                                                               (treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadadr prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) assignments)))
                                                                                               (treemethodhelper (if isconc? hypothesis (cons (caddr prop) hypothesis)) (if isconc? (cons (caddr prop) conclusion) conclusion) assignments)]
                                                                                              [(and (prop-type? (caddr prop) NOT) (not (prop-type? (cadr prop) NOT)))
                                                                                               (treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadr (caddr prop))) (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f) assignments)))
                                                                                               (treemethodhelper (if isconc? hypothesis (cons (cadr prop) hypothesis)) (if isconc? (cons (cadr prop) conclusion) conclusion) assignments)]
                                                                                              [(and (prop-type? (cadr prop) NOT) (prop-type? (caddr prop) NOT))
                                                                                               (treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadadr prop)) (cadadr prop) (symbol->string (cadadr prop))) #f) assignments)))
                                                                                               (treemethodhelper hypothesis conclusion (remove-duplicates (cons (list (if (string? (cadr (caddr prop))) (cadr (caddr prop)) (symbol->string (cadr (caddr prop)))) #f) assignments)))]
                                                                                              )])]))

;;And, finally, time to write the call to take user input and passes it to treemethod.
;;This also negates the conclusion

(print "Please provide input (conclusion hypotheses...): ")(let ([props (read)]) (treemethod (cons (list NOT (car props)) (cdr props))))(println "If a counterexample is not listed, then the inference is valid. However, even though this program will output a counterexample if there is one, it may print the same counterexample multiple times or may miss some.")
