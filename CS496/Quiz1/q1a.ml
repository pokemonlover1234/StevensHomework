
(*
Name: Aidan Fischer
Partner: No partner
Date: 2/17/2020
Pledge: I pledge my honor that I have abided by the Stevens Honor System.
*)

(* Sample Directed Graph *)

let ex = [(1, 2); (2, 3); (3, 1); (3, 4)]


(*
  1 <---- 3
  |     /\ |
  |    /   | 
 \/  /    \/
  2       4
*)
       
(* 
Eg. outgoing ex 3 => [1,4] 
*)
let rec outgoing_nodes (g : (int * int) list) (n : int) : int list =
   List.filter_map (fun (k : int * int) : int option ->
     if (fst k = n) then Some (snd k) else None
   ) g
    
(* 
   The list of nodes of the tree without duplicates. The order of the
   nodes in the list is irrelevant.
   eg. nodes ex => [1,2,3,4] 
*)


let rec nodes g =
   List.sort_uniq (fun a b -> if (a < b) then -1 else if (a = b) then 0 else 1)
   (List.concat @@ List.map (fun (a : (int * int)) : int list -> 
      [fst a; snd a]) g)


(* 
   Remove a node from the graph
   Eg. remove ex 2 =>  [(3, 1); (3, 4)] 
*)
let rec remove g n =
   List.filter (fun (k : (int * int)) : bool -> 
      not (fst k = n || snd k = n)) g
  
(* Reachable nodes from a source node. (Extra-credit)
   Eg. reachale ex 3 => [1,4,2,3] 
   *)

let reachable g (n : int) : int list =
   let rec reachable_helper (cur_reachable : int list) (prev_reachable : int list) : int list = (
      if (cur_reachable = prev_reachable) then cur_reachable else (
          reachable_helper ((List.sort_uniq (fun a b -> if (a < b) then -1 else if (a = b) then 0 else 1)
          (cur_reachable @ List.concat @@ List.map (outgoing_nodes ex) cur_reachable))) cur_reachable
      ) 
   ) in reachable_helper [n;] []
                              