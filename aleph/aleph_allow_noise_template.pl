:- style_check(-discontiguous).

:- set(i,3).
:- set(clauselength,2).
%:- set(minacc,0.8).
%:- set(minscore,1).
:- set(minpos,2).
:- set(nodes,20000).
%:- set(explore,true).
:- set(noise,1).
%:- set(max_features,30).
%:- set(lookahead,2).
:- set(caching, true).

:- set(evalfn, user).
%:- set(search, df).

:- modeh(1,solution(+example)).
:- modeb(*,component_holonym(+example, #word)).
:- modeb(*,member_holonym(+example, #word)).
:- modeb(*,portion_holonym(+example, #word)).
:- modeb(*,related_to(+example, #word)).
:- modeb(*,hypernym(+example, #word)).

:- determination(solution/1, component_holonym/2).
:- determination(solution/1, member_holonym/2).
:- determination(solution/1, portion_holonym/2).
:- determination(solution/1, related_to/2).
:- determination(solution/1, hypernym/2).

% IMPORTANT TO ADD RULES AT THE END
:- ['background.pl'].
:- ['examples.pl'].
:- ['rules.pl'].

has_pieces(true, []) :- !.
has_pieces(','(A, R), [A|Z]) :- has_pieces(R, Z), !.
has_pieces(A, [A]) :- !.


cost(_,[P,_,_],Cost) :-
        Cost = P.

 false :-
    hypothesis(_,Body,_),
    has_pieces(Body,Pieces),
    member(Piece, Pieces),
    arg(2, Piece, Candidate),
    enemy(E),
    %write("Candi: "), write(Candidate), nl,
    %write("Enemy: "), write(E), nl,
    hh(noun(E,_), noun(Candidate,_)),
    write("CONSTRAINT 2: "), write(Candidate), write("/"), write(E), write(" Enemy was included in solution."), nl.

% constraint prevents that the given words will be part of the solution.
false :-
    hypothesis(_,Body,_),
    has_pieces(Body,Pieces),
    word(W),
    (member( hypernym(_, W), Pieces); member( component_holonym(_, W), Pieces); member( member_holonym(_, W), Pieces); member( portion_holonym(_, W), Pieces) ),
    write("CONSTRAINT: "), write(W), write(Pieces), write("No word is allowed which belongs to given list."), nl.





