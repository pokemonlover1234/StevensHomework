%%% Stub for Quiz 6

%%% Name: Aidan Fischer  No Partner
%%% I pledge my honor that I have abided by the Stevens Honor System.
-module(calc).
-compile(export_all).

env() -> #{"x"=>3, "y"=>7}.

e1() ->
    {add, 
     {const,3},
     {divi,
      {var,"x"},
      {const,4}}}.

e2() ->
    {add, 
     {const,3},
     {divi,
      {var,"x"},
      {const,0}}}.

e3() ->
    {add, 
     {const,3},
     {divi,
      {var,"r"},
      {const,4}}}.

calc({const,N},_E) ->
    {val,N};

calc({var,Id},E) ->
    case maps:find(Id,E) of
        error -> throw(unbound_identifier_error);
        {ok, Value} -> {val,Value}
    end;

calc({add,E1,E2},E) ->
    {val,N} = calc(E1,E),
    {val,M} = calc(E2,E),
    {val,N + M};

calc({sub,E1,E2},E) ->
    {val,N} = calc(E1,E),
    {val,M} = calc(E2,E),
    {val,N - M};

calc({mult,E1,E2},E) ->
    {val,N} = calc(E1,E),
    {val,M} = calc(E2,E),
    {val, N * M};

calc({divi,E1,E2},E) ->
    {val,N} = calc(E1,E),
    {val,M} = calc(E2,E),
    case M of
        0 -> throw(division_by_zero_error);
        _V when _V /= 0 -> {val, N div M}
    end.

