-module(server).

-export([start_server/0]).

-include_lib("./defs.hrl").

-spec start_server() -> _.
-spec loop(_State) -> _.
-spec do_join(_ChatName, _ClientPID, _Ref, _State) -> _.
-spec do_leave(_ChatName, _ClientPID, _Ref, _State) -> _.
-spec do_new_nick(_State, _Ref, _ClientPID, _NewNick) -> _.
-spec do_client_quit(_State, _Ref, _ClientPID) -> _NewState.

%% Name: Aidan Fischer
%% I pledge my honor that I have abided by the Stevens Honor System.

start_server() ->
    catch(unregister(server)),
    register(server, self()),
    case whereis(testsuite) of
	undefined -> ok;
	TestSuitePID -> TestSuitePID!{server_up, self()}
    end,
    loop(
      #serv_st{
	 nicks = maps:new(), %% nickname map. client_pid => "nickname"
	 registrations = maps:new(), %% registration map. "chat_name" => [client_pids]
	 chatrooms = maps:new() %% chatroom map. "chat_name" => chat_pid
	}
     ).

loop(State) ->
    receive 
	%% initial connection
	{ClientPID, connect, ClientNick} ->
	    NewState =
		#serv_st{
		   nicks = maps:put(ClientPID, ClientNick, State#serv_st.nicks),
		   registrations = State#serv_st.registrations,
		   chatrooms = State#serv_st.chatrooms
		  },
	    loop(NewState);
	%% client requests to join a chat
	{ClientPID, Ref, join, ChatName} ->
	    NewState = do_join(ChatName, ClientPID, Ref, State),
	    loop(NewState);
	%% client requests to join a chat
	{ClientPID, Ref, leave, ChatName} ->
	    NewState = do_leave(ChatName, ClientPID, Ref, State),
	    loop(NewState);
	%% client requests to register a new nickname
	{ClientPID, Ref, nick, NewNick} ->
	    NewState = do_new_nick(State, Ref, ClientPID, NewNick),
	    loop(NewState);
	%% client requests to quit
	{ClientPID, Ref, quit} ->
	    NewState = do_client_quit(State, Ref, ClientPID),
	    loop(NewState);
	{TEST_PID, get_state} ->
	    TEST_PID!{get_state, State},
	    loop(State)
    end.

%% executes join protocol from server perspective
do_join(ChatName, ClientPID, Ref, State) ->
    case maps:is_key(ChatName, State#serv_st.chatrooms) of
		false -> RoomPID = spawn(chatroom, start_chatroom, [ChatName]);
		true -> RoomPID = maps:get(ChatName, State#serv_st.chatrooms)
	end,
	ClientNick = maps:get(ClientPID, State#serv_st.nicks),
	RoomPID ! {self(), Ref, register, ClientPID, ClientNick},
	State#serv_st{registrations = maps:update_with(ChatName, fun(ClientList) ->
		[ClientPID] ++ ClientList
	end, [ClientPID], State#serv_st.registrations), chatrooms = 
	case maps:is_key(ChatName, State#serv_st.chatrooms) of 
		true -> State#serv_st.chatrooms;
		false -> maps:put(ChatName, RoomPID, State#serv_st.chatrooms)
	end}.

%% executes leave protocol from server perspective
do_leave(ChatName, ClientPID, Ref, State) ->
    RoomPID = maps:get(ChatName, State#serv_st.chatrooms),
	RoomPID ! {self(), Ref, unregister, ClientPID},
	ClientPID ! {self(), Ref, ack_leave},
	State#serv_st{registrations = maps:update_with(ChatName, fun(ClientList)->
		lists:delete(ClientPID, ClientList)
	end, State#serv_st.registrations)}.

%% executes new nickname protocol from server perspective
do_new_nick(State, Ref, ClientPID, NewNick) ->
    case lists:member(NewNick, maps:values(State#serv_st.nicks)) of
		true ->
			ClientPID ! {self(), Ref, err_nick_used}, State;
		false ->
			lists:foreach(fun(RoomPID) ->
				RoomPID ! {self(), Ref, update_nick, ClientPID, NewNick}
			end, maps:values(State#serv_st.chatrooms)),
			ClientPID ! {self(), Ref, ok_nick},
			State#serv_st{nicks = maps:update(ClientPID, NewNick, State#serv_st.nicks)}
	end.

%% executes client quit protocol from server perspective
do_client_quit(State, Ref, ClientPID) ->
	lists:foreach(fun(RoomPID) ->
		RoomPID ! {self(), Ref, unregister, ClientPID}
	end, maps:values(maps:filter(fun(ChatName, _RoomPID) -> 
		lists:member(ClientPID, maps:get(ChatName, State#serv_st.registrations))
	end, State#serv_st.chatrooms))),
	State#serv_st{nicks = maps:remove(ClientPID, State#serv_st.nicks),
	              registrations = maps:map(fun(_, ClientList) -> 
					lists:delete(ClientPID, ClientList)	  
				  end, State#serv_st.registrations)}.
