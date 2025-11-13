% prevent warnings because these predicates are defined in different files.
:- multifile hypernym/2.
:- multifile component_holonym/2.
:- multifile member_holonym/2.
:- multifile portion_holonym/2.
:- multifile related_to/2.

% helper predicates to represent a recursive structure.
hh(A,D) :- has_hypernym(A,D).
hh(A,D) :- has_hypernym(A,B), hh(B,D).

hc(A,D) :- has_component_holonym(A,D).
hc(A,D) :- has_component_holonym(A,B), hh(B,D).

hm(A,D) :- has_member_holonym(A,D).
hm(A,D) :- has_member_holonym(A,B), hh(B,D).

hp(A,D) :- has_portion_holonym(A,D).
hp(A,D) :- has_portion_holonym(A,B), hh(B,D).

hr(A,D) :- is_related_to(A,D).
hr(A,D) :- is_related_to(A,B), hh(B,D).



hypernym(E,W) :-
    findall(Origin, clause(hypernym(E,Origin), _), [Origin|_]),
    hh(noun(X,_),noun(W,_)),
    X == Origin.

component_holonym(E,W) :-
    findall(Origin, clause(component_holonym(E,Origin), _), [Origin|_]),
    hc(noun(X,_),noun(W,_)),
    X == Origin.

member_holonym(E,W) :-
    findall(Origin, clause(member_holonym(E,Origin), _), [Origin|_]),
    hm(noun(X,_),noun(W,_)),
    X == Origin.

portion_holonym(E,W) :-
    findall(Origin, clause(portion_holonym(E,Origin), _), [Origin|_]),
    hp(noun(X,_),noun(W,_)),
    X == Origin.

related_to(E,W) :-
    findall(Origin, clause(related_to(E,Origin), _), [Origin|_]),
    hr(noun(X,_),noun(W,_)),
    X == Origin.

