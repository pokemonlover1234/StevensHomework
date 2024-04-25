(* 

   HW2 
   Please
   1. Rename to gt.ml
   2. Place the names of the group members here:

    Name1: Aidan Fischer
    Name2: N/A

  I pledge my honor that I have abided by the Stevens Honor System
*)



type 'a gt = Node of 'a*('a gt) list

let mk_leaf (n:'a) : 'a gt =
  Node(n,[])
    
let t : int gt =
 Node (33,
       [Node (12,[]);
        Node (77, 
              [Node (37, 
                     [Node (14, [])]); 
               Node (48, []); 
               Node (103, [])])
       ])

(*Get max element of a list guaranteed to have all elements >= 0*)
let rec maxp l = 
  match l with
  | [] -> 0
  | h::t -> let k = maxp t in if (h>k) then h else k

let rec height t =
  match t with
  | Node(d, []) -> 1
  | Node(d, l) -> maxp (List.map (fun k -> height k) l) + 1
    
let rec size t =
  match t with
  | Node(d, []) -> 1
  | Node(d, l) -> 1 + List.fold_left (fun a b -> a + b) 0 (List.map size l)


let rec paths_to_leaves t: int list list =
  match t with
  | Node(d, []) -> [[]]
  | Node(d, l) -> List.fold_left (fun a b -> a @ b) [] 
    (List.mapi (fun i k -> 
      List.map (fun l -> i::l) (paths_to_leaves k)) l)


let rec is_perfect t =
  let paths = paths_to_leaves t in List.for_all (fun k -> List.length k = List.length @@ List.hd @@ paths) paths


let rec preorder (Node(d,ch)) =
    match ch with
    | [] -> [d]
    | h::t -> [d] @ List.fold_left (fun a b -> a @ b) [] (List.map preorder (h::t))

                        
let rec mirror (Node(d,ch)) =
  match ch with
  | [] -> Node(d, [])
  | h::t -> Node(d, List.rev_map mirror ch)

  
let rec mapt f (Node(d,ch)) =
  match ch with
  | [] -> Node(f d, [])
  | h::t -> Node (f d, List.map (mapt f) ch)
  
let rec foldt : ('a -> 'b list -> 'b) -> 'a gt -> 'b =
  fun f (Node(d,ch)) ->
    f d (List.map (fun k -> foldt f k) ch)

let sumt t =
  foldt (fun i rs -> i + List.fold_left (fun i j -> i+j) 0 rs) t

let memt t e = 
  foldt (fun i rs -> i=e || List.exists (fun i -> i) rs) t

let mirror' t  = 
  foldt (fun i rs -> Node(i,List.rev rs)) t
