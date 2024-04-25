%% Intro to Erlang
%% 25 Oct 2021

-module(ex).
-compile(export_all).
-author("E.B").


start() ->
    io:format("hello~n").




%% {empty} - empty tree
%% {node,Data,LT,RT} - non-empty tree

  %%  20
  %% /  \
  %% 4    77
  %%     /
  %%    33


    
aTree() ->
    {node,20,
         {node,4,{empty},{empty}},
         {node,77,
	         {node,33,{empty},{empty}},
                 {empty}}}.

sumT({empty}) ->
    0;
sumT({node,D,LT,RT}) ->
     D + sumT(LT) + sumT(RT).


  %%  20
  %% /  \
  %% 77   4
  %%   \  
  %%   33

mirror({empty}) ->
    {empty};
mirror({node,D,LT,RT}) ->
    {node,D,mirror(RT),mirror(LT)}.

sumL([]) ->
    0;
sumL([H | T]) ->
    H + sumL(T).

stutter([]) ->
    [];
stutter([H | T]) ->
    [ H | [ H | stutter(T)]].



last([H]) ->
    H;
last([ _H1 | [ H2 | T]]) ->
    last([H2|T]);
last(_) ->
    error.  

rev([]) ->
    [];
rev([H | T]) ->
    rev(T) ++ [H].

frev([],A) ->
    A;
frev([H|T],A) ->
    frev(T,[H|A]).

%%% ino/
%%% Computer the inorder traversal of a binary tree
%%% Eg.
%%% ex:ino(ex:aTree()) => [4,20,33,77]

ino({empty}) -> 
    [];
ino({node,D,LT,RT}) -> 
    ino(LT) ++ [D | ino(RT)].

%%%

%% Summary of today's lecture on Erlang

%% erl is the command to run the shell
%% Get out with q().
%% Expressions:
%%   Atoms
%%   Numbers
%%   Lists
%%   Strings
%% Pattern matching
%% Recursion
%% Matching operator (=)
%% NO ASSIGNMENT!!!




