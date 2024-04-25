-module(dc).
-compile(export_all).
	
%% Name: Aidan Fischer/No Partner
%% I pledge my honor that I have abided by the Stevens Honor System.
start(E,M) ->
    S=spawn(?MODULE,dryCleaner,[0,0]),
    [ spawn(?MODULE,employee,[S]) || _ <- lists:seq(1,E) ],
    [ spawn(?MODULE,dryCleanMachine,[S]) || _ <- lists:seq(1,M) ].
    

dryCleaner(Clean,Dirty) -> %% Clean, Dirty are counters
    io:format("Clean ~p, Dirty ~p ~n",[Clean,Dirty]),
    receive
        {dropOffOverall} -> dryCleaner(Clean, Dirty + 1);
        {From,dryCleanItem} when Dirty > 0 -> 
            From ! {continue}, dryCleaner(Clean + 1, Dirty - 1);
        {From, pickUpOverall} when Clean > 0 ->
            From ! {continue}, dryCleaner(Clean - 1, Dirty)
   end.
employee(DC) -> % drop off overall, then pick up a clean one (if none
                % is available, wait), and end
    DC ! {dropOffOverall},
    DC ! {self(), pickUpOverall},
    receive
        {continue} -> ok
    end.

dryCleanMachine(DC) ->  % dry clean item (if none are available, wait),
                        % then sleep for 1000 milliseconds and repeat
    DC ! {self(), dryCleanItem},
    receive
        {continue} -> timer:sleep(1000), dryCleanMachine(DC)
    end.


