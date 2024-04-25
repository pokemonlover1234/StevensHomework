-module(barr).
-compile(export_all).

start() ->
    B = spawn(?MODULE,loop,[2,2,[]]),
    spawn(?MODULE,client1,[B]),
    spawn(?MODULE,client2,[B]),
    ok.

loop(N,0,L) -> 
    lists:foreach(fun({Pid,R}) ->
        Pid!{ok, R}
    end, L);
loop(N,M,L) -> 
    receive
        {Pid, R} -> loop(N, M - 1, lists:append(L, [{Pid, R}]))
    end.

reached(B) ->
    R = make_ref(),
    B ! {self(), R},
    receive
        {ok, R} ->
            observer_backend
    end.


client1(B) ->
    io:format("a~n"),
    reached(B),
    io:format("1~n").

client2(B) ->
    io:format("b~n"),
    reached(B),
    io:format("2~n").