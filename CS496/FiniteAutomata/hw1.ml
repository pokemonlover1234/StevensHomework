
(*
Name: Aidan Fischer
Date: 2/17/2020
Pledge: I pledge my honor that I have abided by the Stevens Honor System.
*)

(* ******************************************** *)
(** Basic functions on finite automata *)
(* ******************************************** *)
(**
   Code stub for assignment 1
*)

type symbol = char
type input = char list

type state = string

(* transition function *)
type tf = (state * symbol * state) list

(* initial state * transition function * end state *)
type fa = { states: state list; start:state; tf: tf; final: state list}


(* ******************************************** *)
(* Examples of automata *)
(* ******************************************** *)

let a = {states = ["q0";"q1";"q2"];
         start = "q0";
         tf = [("q0",'a',"q1"); ("q1",'b',"q1"); ("q1",'c',"q2")];
         final = ["q2"]}

let a2 = {states = ["q0";"q1";"q2";"q3";"q4"];
          start = "q0";
          tf = [("q0",'a',"q1"); ("q1",'b',"q1")
               ; ("q1",'c',"q2");  ("q3",'a',"q4")];
          final= ["q2";"q3"]
         }
let tf_of_a = [("q0",'a',"q1"); ("q1",'b',"q1"); ("q1",'c',"q2")]

let non_det = {states = ["q0";"q1";"q2";"q3"];
               start = "q0";
               tf = [("q0",'a',"q1"); ("q0", 'a', "q3"); ("q1",'b',"q1"); 
               ("q1",'c',"q2")];
               final= ["q2";"q3"]}

let non_val = {states = ["q0";"q1";"q2"];
               start = "q3";
               tf = [("q0",'a',"q1"); ("q1",'b',"q1"); ("q1",'c',"q2")];
               final = ["q2"]}

let non_val2 = {states = ["q0";"q1";"q2"];
                start = "q0";
                tf = [("q0",'a',"q1"); ("q1",'b',"q1"); ("q1",'c',"q2")];
                final = ["q2";"q3"]}
(* ******************************************** *)
(* Helper functions *)
(* ******************************************** *)

let input_of_string s =
  let rec exp i l =
    if i < 0 then l else exp (i - 1) (s.[i] :: l) in
  exp (String.length s - 1) []

(*next takes a transition function, state and symbol, and returns a list of states representing the
  results of the transition function on that symbol and state*)
let next (f : tf) (st : state) (sy : symbol) : state list = 
  (*check_transition is a predicate function that checks if the transition 
    (in the transition function) matches the input. *)
  let check_transition (tr : (state * symbol * state)) : bool = (
    match tr with
      | (a,b,c) when a = st && b = sy -> true
      | _ -> false
  (*Rather than just return the first entry, filter the transition function
    and then map the results through a function that extracts the result states.
    This is so we can check for non-determinism*)
  ) in let transitions = List.filter check_transition f in 
  List.map (fun (tr : (state * symbol * state)) -> 
    match tr with
    | (a,b,c) -> c) transitions

(*get_alphabet is a helper function that extracts all possible symbols for a
  finite automata from a given transition function*)
let rec get_alphabet (f : tf) : symbol list = 
  match f with 
  | [] -> []
  | (a,b,c)::t -> let r = get_alphabet t in if (List.mem b r) then r else b :: r

(* ******************************************** *)
(* Simulating automata *)
(* ******************************************** *)
(*Applies the transition function f on the given state and symbol, assuming a 
  deterministic machine*)
let apply_transition_function (f : tf) (st : state) (sy : symbol) : state option = 
  let transition = next f st sy in 
    if (List.length transition = 0) then None else 
      Some (List.hd transition)

 (*Runs input through the given automata, assuming a deterministic machine. Returns
 true if the machine ends on an accept state, false otherwise*)
let accept (automata : fa) (inp : input) : bool = 
  (*accept_helper recurses through the input, returning false if we ever get to
  an invalid state (apply_transition_function returned None) or we complete 
  processing the input and the state isn't an accept state. Returns true if
  and only if the input is processed and no invalid transitions are requested
  , and the final state reached is an accept state. *)
  let rec accept_helper (cur_state : state option) (rem_inp : input) = (
    if (cur_state = None) then false else 
      match rem_inp with 
      (*We can safely Option.get here since we make sure cur_state isn't none
    with the preceding if.*)
      | [] -> List.mem (Option.get cur_state) automata.final
      (*We have more input to process, so apply the transition function and continue*)
      | h::t -> accept_helper (apply_transition_function automata.tf (Option.get cur_state) h) t
  ) in accept_helper (Some automata.start) inp

(*Determins if a given automata is deterministic by checking if there is any state/symbol
  combination that, when passed through the transition function, returns multiple transitions*)
let deterministic (automata : fa) = 
  (*For each symbol in the alphabet, for each state in the automata, make sure no
  more than one state is returned by the transition function on that symbol/state*)
  List.for_all (fun (k : symbol) -> 
    List.for_all (fun (st : state) ->
      List.length (next automata.tf st k) <= 1) automata.states) (get_alphabet automata.tf)

(*Checks if a given automata is "valid", with that start state and final state(s)
  in the given set of states, and that it is deterministic*)
let valid (automata : fa) : bool = 
  (List.mem automata.start automata.states) &&
  (List.for_all (fun (k : state) -> 
    List.mem k automata.states) automata.final) &&
  deterministic automata

(*Determines which states in fa are reachable from the start state through the
  transition function*)
let reachable (automata : fa) : state list =
  (*Get the next possible states from a list of states*)
  let rec get_next_states (states : state list) : state list = (
    match states with
    | [] -> []
    | h::t -> List.filter_map (fun (k : symbol) : state option -> (
      apply_transition_function automata.tf h k
    )) (get_alphabet automata.tf) @ (get_next_states t)
  (*Continuously process the list of possible states through get_next_states. sort_uniq 
    makes sure the lists are always in a predictable order AND that they contain unique 
    elements. This allows us to determine when no new states are reached, when cur_states
    and prv_states are equal*)
  ) in let rec reachable_helper (cur_states : state list) (prev_states : state list) : state list = (
    if cur_states = prev_states then cur_states else
      let next_states = List.sort_uniq 
        (fun a b -> if (a < b) then -1 else if (a = b) then 0 else -1)
        (cur_states @ (get_next_states cur_states)) in reachable_helper next_states cur_states
  ) in reachable_helper [automata.start;] []

(*Uses reachable to filter unreachable states out of the properties of a finite automata*)
let remove_dead_states (automata : fa) : fa =
  let reachable_states = reachable automata in {
    states = reachable_states;
    start = automata.start;
    tf = List.filter (fun (k : (state * symbol * state)) : bool -> 
      match k with
      | (a,b,c) -> List.mem a reachable_states && List.mem c reachable_states
    ) automata.tf;
    final = List.filter (fun (k : state) : bool -> 
      List.mem k reachable_states
    ) automata.final
  }