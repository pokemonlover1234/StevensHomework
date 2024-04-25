-module(shipping).
-compile(export_all).
-include_lib("./shipping.hrl").
%Name: Aidan Fischer. No Partner.
%I pledge my honor that I have abided by the Stevens Honor System.
get_ship(Shipping_State, Ship_ID) ->
    case lists:keyfind(Ship_ID, #ship.id, Shipping_State#shipping_state.ships) of
        false -> error;
        T when T =/= false -> #ship{id = T#ship.id, name = T#ship.name, container_cap = T#ship.container_cap}
    end.

get_container(Shipping_State, Container_ID) ->
    case lists:keyfind(Container_ID, #container.id, Shipping_State#shipping_state.containers) of
        false -> error;
        T when T =/= false -> #container{id = T#container.id, weight = T#container.weight}
    end.

get_port(Shipping_State, Port_ID) ->
    case lists:keyfind(Port_ID, #port.id, Shipping_State#shipping_state.ports) of
        false -> error;
        T when T =/= false -> #port{id = T#port.id, name = T#port.name, docks = T#port.docks, container_cap = T#port.container_cap}
    end.

get_occupied_docks(Shipping_State, Port_ID) ->
    Locs = lists:filter(fun(T) -> 
        {Port, _Dock, _Ship} = T,
        Port == Port_ID   
    end, Shipping_State#shipping_state.ship_locations),
    {_Port, Docks, _Ships} = lists:unzip3(Locs),
    Docks.

get_ship_location(Shipping_State, Ship_ID) ->
    case lists:search(fun(T) ->
        {_Port, _Dock, Ship} = T,
        Ship == Ship_ID
    end, Shipping_State#shipping_state.ship_locations) of
        false -> error;
        {value, {Port, Dock, _Ship}} -> {Port, Dock}
    end.

get_container_weight(Shipping_State, Container_IDs) ->
    Weights = lists:map(fun(T) ->
        C = get_container(Shipping_State, T),
        case C of
            error -> error;
            V when V =/= error -> V#container.weight
        end
    end, Container_IDs),
    case lists:member(error, Weights) of
        true -> error;
        false -> lists:sum(Weights)
    end.

get_ship_weight(Shipping_State, Ship_ID) ->
    case get_ship(Shipping_State, Ship_ID) of
        error -> error;
        _V when _V =/= error -> {ok, IDs} = maps:find(Ship_ID,Shipping_State#shipping_state.ship_inventory),
        get_container_weight(Shipping_State, IDs)
    end.

load_ship(Shipping_State, Ship_ID, Container_IDs) ->
    case get_ship_location(Shipping_State, Ship_ID) of 
        error -> error;
        {Loc_Port, _Loc_Dock} ->
            {ok,Inv} = maps:find(Loc_Port, Shipping_State#shipping_state.port_inventory),
            case lists:all(fun(Container_ID) ->
                lists:member(Container_ID, Inv)
            end, Container_IDs) of 
                false -> error;
                true -> 
                    Ship = get_ship(Shipping_State, Ship_ID),
                    New_State = Shipping_State#shipping_state{
                        ship_inventory = maps:update_with(Ship_ID,fun(IDs) ->
                            IDs ++ Container_IDs
                        end, Shipping_State#shipping_state.ship_inventory),
                        port_inventory = maps:update_with(Loc_Port,fun(IDs) ->
                            lists:subtract(IDs, Container_IDs)
                        end, Shipping_State#shipping_state.port_inventory)
                    },
                    case maps:find(Ship_ID, New_State#shipping_state.ship_inventory) of
                        {ok, ContainerList} when length(ContainerList) > Ship#ship.container_cap -> error;
                        _ -> New_State
                    end
            end
    end.

unload_ship_all(Shipping_State, Ship_ID) ->
    Ship_Loc = get_ship_location(Shipping_State, Ship_ID),
    case Ship_Loc of
        error -> error;
        {Ship_Port, _Ship_Dock} -> 
            {ok,Ship_Containers} = maps:find(Ship_ID, Shipping_State#shipping_state.ship_inventory),
            {ok,Port_Containers} = maps:find(Ship_Port, Shipping_State#shipping_state.port_inventory),
            Port = get_port(Shipping_State, Ship_Port),
            if length(Ship_Containers) + length(Port_Containers) > Port#port.container_cap ->
                error;
            true ->
                Shipping_State#shipping_state{ship_inventory = maps:update(Ship_ID, [], 
                    Shipping_State#shipping_state.ship_inventory), 
                    port_inventory = maps:update_with(Ship_Port, fun(IDs) ->
                        IDs ++ Ship_Containers
                    end, Shipping_State#shipping_state.port_inventory)}
            end
    end.

unload_ship(Shipping_State, Ship_ID, Container_IDs) ->
    case get_ship_location(Shipping_State, Ship_ID) of 
        error -> error;
        {Loc_Port, _Loc_Dock} ->
            {ok,Inv} = maps:find(Ship_ID, Shipping_State#shipping_state.ship_inventory),
            case lists:all(fun(Container_ID) ->
                lists:member(Container_ID, Inv)
            end, Container_IDs) of 
                false -> error;
                true -> 
                    Port = get_port(Shipping_State, Loc_Port),
                    New_State = Shipping_State#shipping_state{
                        ship_inventory = maps:update_with(Ship_ID,fun(IDs) ->
                            lists:subtract(IDs, Container_IDs)
                        end, Shipping_State#shipping_state.ship_inventory),
                        port_inventory = maps:update_with(Loc_Port,fun(IDs) ->
                            IDs ++ Container_IDs
                        end, Shipping_State#shipping_state.port_inventory)
                    },
                    case maps:find(Loc_Port, New_State#shipping_state.port_inventory) of
                        {ok, ContainerList} when length(ContainerList) > Port#port.container_cap -> error;
                        _ -> New_State
                    end
            end
    end.

set_sail(Shipping_State, Ship_ID, {Port_ID, Dock}) ->
    case get_ship(Shipping_State, Ship_ID) of 
        error -> error;
        Ship when Ship =/= error ->
        case get_port(Shipping_State, Port_ID) of
            error -> error;
            Port when Port =/= error ->
                Occupied = get_occupied_docks(Shipping_State, Port_ID),
                case lists:member(Dock, Occupied) of
                    true -> error;
                    false ->
                        {Ship_Port, Ship_Dock} = get_ship_location(Shipping_State, Ship_ID),
                        Shipping_State#shipping_state{ship_locations = lists:map(fun(Loc) ->
                            case Loc of
                                {Ship_Port, Ship_Dock, Ship_ID} -> {Port_ID, Dock, Ship_ID};
                                Else -> Else
                            end
                        end, Shipping_State#shipping_state.ship_locations)}
                end
        end
    end.



%% Determines whether all of the elements of Sub_List are also elements of Target_List
%% @returns true is all elements of Sub_List are members of Target_List; false otherwise
is_sublist(Target_List, Sub_List) ->
    lists:all(fun (Elem) -> lists:member(Elem, Target_List) end, Sub_List).




%% Prints out the current shipping state in a more friendly format
print_state(Shipping_State) ->
    io:format("--Ships--~n"),
    _ = print_ships(Shipping_State#shipping_state.ships, Shipping_State#shipping_state.ship_locations, Shipping_State#shipping_state.ship_inventory, Shipping_State#shipping_state.ports),
    io:format("--Ports--~n"),
    _ = print_ports(Shipping_State#shipping_state.ports, Shipping_State#shipping_state.port_inventory).


%% helper function for print_ships
get_port_helper([], _Port_ID) -> error;
get_port_helper([ Port = #port{id = Port_ID} | _ ], Port_ID) -> Port;
get_port_helper( [_ | Other_Ports ], Port_ID) -> get_port_helper(Other_Ports, Port_ID).


print_ships(Ships, Locations, Inventory, Ports) ->
    case Ships of
        [] ->
            ok;
        [Ship | Other_Ships] ->
            {Port_ID, Dock_ID, _} = lists:keyfind(Ship#ship.id, 3, Locations),
            Port = get_port_helper(Ports, Port_ID),
            {ok, Ship_Inventory} = maps:find(Ship#ship.id, Inventory),
            io:format("Name: ~s(#~w)    Location: Port ~s, Dock ~s    Inventory: ~w~n", [Ship#ship.name, Ship#ship.id, Port#port.name, Dock_ID, Ship_Inventory]),
            print_ships(Other_Ships, Locations, Inventory, Ports)
    end.

print_containers(Containers) ->
    io:format("~w~n", [Containers]).

print_ports(Ports, Inventory) ->
    case Ports of
        [] ->
            ok;
        [Port | Other_Ports] ->
            {ok, Port_Inventory} = maps:find(Port#port.id, Inventory),
            io:format("Name: ~s(#~w)    Docks: ~w    Inventory: ~w~n", [Port#port.name, Port#port.id, Port#port.docks, Port_Inventory]),
            print_ports(Other_Ports, Inventory)
    end.
%% This functions sets up an initial state for this shipping simulation. You can add, remove, or modidfy any of this content. This is provided to you to save some time.
%% @returns {ok, shipping_state} where shipping_state is a shipping_state record with all the initial content.
shipco() ->
    Ships = [#ship{id=1,name="Santa Maria",container_cap=20},
              #ship{id=2,name="Nina",container_cap=20},
              #ship{id=3,name="Pinta",container_cap=20},
              #ship{id=4,name="SS Minnow",container_cap=20},
              #ship{id=5,name="Sir Leaks-A-Lot",container_cap=20}
             ],
    Containers = [
                  #container{id=1,weight=200},
                  #container{id=2,weight=215},
                  #container{id=3,weight=131},
                  #container{id=4,weight=62},
                  #container{id=5,weight=112},
                  #container{id=6,weight=217},
                  #container{id=7,weight=61},
                  #container{id=8,weight=99},
                  #container{id=9,weight=82},
                  #container{id=10,weight=185},
                  #container{id=11,weight=282},
                  #container{id=12,weight=312},
                  #container{id=13,weight=283},
                  #container{id=14,weight=331},
                  #container{id=15,weight=136},
                  #container{id=16,weight=200},
                  #container{id=17,weight=215},
                  #container{id=18,weight=131},
                  #container{id=19,weight=62},
                  #container{id=20,weight=112},
                  #container{id=21,weight=217},
                  #container{id=22,weight=61},
                  #container{id=23,weight=99},
                  #container{id=24,weight=82},
                  #container{id=25,weight=185},
                  #container{id=26,weight=282},
                  #container{id=27,weight=312},
                  #container{id=28,weight=283},
                  #container{id=29,weight=331},
                  #container{id=30,weight=136}
                 ],
    Ports = [
             #port{
                id=1,
                name="New York",
                docks=['A','B','C','D'],
                container_cap=200
               },
             #port{
                id=2,
                name="San Francisco",
                docks=['A','B','C','D'],
                container_cap=200
               },
             #port{
                id=3,
                name="Miami",
                docks=['A','B','C','D'],
                container_cap=200
               }
            ],
    %% {port, dock, ship}
    Locations = [
                 {1,'B',1},
                 {1, 'A', 3},
                 {3, 'C', 2},
                 {2, 'D', 4},
                 {2, 'B', 5}
                ],
    Ship_Inventory = #{
      1=>[14,15,9,2,6],
      2=>[1,3,4,13],
      3=>[],
      4=>[2,8,11,7],
      5=>[5,10,12]},
    Port_Inventory = #{
      1=>[16,17,18,19,20],
      2=>[21,22,23,24,25],
      3=>[26,27,28,29,30]
     },
    #shipping_state{ships = Ships, containers = Containers, ports = Ports, ship_locations = Locations, ship_inventory = Ship_Inventory, port_inventory = Port_Inventory}.
