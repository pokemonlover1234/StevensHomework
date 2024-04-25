(*
Name: Aidan Fischer
No partner
Quiz 2
I pledge my honor that I have abided by the Stevens Honor System.
*)


(* Recursion on numbers *)

let rec fact n =
  match n with
  | 0 -> 1
  | m when m>0 -> m * fact (m-1)
  | _ -> failwith "negative argument"

let rec f (e:'a) (n:int) : 'a list =
  match n with
  | 0 -> []
  | m -> e :: f e (m-1)


(* Recursion on lists *)

let rec size (l:'a list) : int =
  match l with
  | [] -> 0
  | _::t -> 1 + size t

let rec suml (l:int list) : int =
  match l with
  | [] -> 0
  | h::t -> h + suml t

let rec suml' : int list -> int =
  function
  | [] -> 0
  | h::t -> h + suml' t

let rec suml'' : int list -> int =
  fun l ->
  match l with
  | [] -> 0
  | h::t -> h + suml'' t

(** [mem e l] returns true if [e] belongs to [l], and false oth. *)
(* 
mem 1 [1;2;3] ==> true
mem 7 [1;2;3] ==> false 
*)
let rec mem e l =
  match l with
  | [] -> false
  | h::t ->
    if h=e
    then true
    else mem e t

let rec mem' e l =
  match l with
  | [] -> false
  | h::t -> h=e || mem' e t

(** [rev l] returns the reverse of [l] *) 
let rec rev l =
  match l with
  | [] -> []
  | h::t ->  rev t @ [h]

let rec rev' l a =
  match l with
  | [] -> a
  | h::t -> rev' t (h::a)

(*
stutter [] ==> []
stutter [2;1;3] ==> [2;2;1;1;3;3]
*)
let rec stutter l =
  match l with
  | [] -> []
  | h::t -> h::h::stutter t
    
let has_size_at_least_two l =
  match l with
  | _::_::_ -> true
  | _ -> false
    
(* 
rad [] ==> []
rad [1] ==> [1]
rad [1;2;2;2;3;3;4] ==> [1;2;3;4]
*)
let rec remove_adj_duplicates l =
  match l with
  | [] -> []
  | a::b::t when a=b -> remove_adj_duplicates (b::t)
  | a::b::t when a<>b -> a::remove_adj_duplicates (b::t)
  | h::t -> h::t

     
(* Well-known higher-order function schemes *)


let succ i = i+1
let upper c = Char.uppercase_ascii c
let is_zero i = i=0
                
(* increments each number in l by one and returns the resulting list *)
let rec succl l =
  match l with
  | [] -> []
  | h::t -> succ h :: succl t

let rec upperl l =
  match l with
  | [] -> []
  | h::t -> upper h :: upperl t

let rec testzl l =
  match l with
  | [] ->[]
  | h::t -> is_zero h :: testzl t


let rec map (f:'a->'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | h::t -> f h :: map f t

let rec succl' = map succ
let rec upperl' = map upper
let rec testzl' = map is_zero


let is_positive i = i>0
let is_upper i = i = Char.uppercase_ascii i
let isne i = i<>[]
                
(* retains those numbers in l that are gtz; it throws the others away *)
let rec greater_than_zero l =
  match l with
  | [] -> []
  | h::t ->
    if is_positive h
    then h :: greater_than_zero t
    else greater_than_zero t

let rec get_upper l =
  match l with
  | [] -> []
  | h::t ->
    if is_upper h
    then h :: get_upper t
    else get_upper t
          
let rec get_non_empty l =
  match l with
  | [] -> []
  | h::t ->
    if isne h
    then h :: get_non_empty t
    else get_non_empty t

let rec filter (p:'a->bool) (l:'a list) : 'a list = 
  match l with
  | [] -> []
  | h::t ->
    if p h
    then h :: filter p t
    else filter p t

let greater_than_zero' = filter is_positive
let get_upper' = filter is_upper
let get_non_empty' = filter isne


(* conjunction of the all the booleans in l *)
let rec andl l =
  match l with
  | [] -> true
  | h::t -> h && andl t
              
let rec suml l =
  match l with
  | [] -> 0
  | h::t -> h + suml t

let rec concat l =
  match l with
  | [] -> []
  | h::t -> h @ concat t

let rec foldr (f:'a->'b->'b)  (a:'b) (l:'a list) : 'b =
  match l with
  | [] -> a
  | h::t -> f h (foldr f a t)

let rec foldl (f:'a->'b->'b)  (a:'b) (l:'a list) : 'b =
  match l with
  | [] -> a
  | h::t -> foldl f (f a h) t


let andl' = foldr (fun h r -> h && r) true 
let suml'  = foldr (fun h r -> h+r) 0 
let concat' = foldr (fun h r -> h @ r) []

(* Algebraic Data Types *)

type dot = Mon | Tue | Wed | Thu | Fri | Sat | Sun

let is_weekend d =
  match d with
  | Sat | Sun -> true
  | _ -> false

type flavor = Choc | Straw | Van
type icecream = Cup of flavor | Cone of flavor*flavor

let ic1 = Cup(Choc)
let ic2 = Cone(Choc,Straw)
    
let is_boring ic =
  match ic with
  | Cup(_) -> false
  | Cone(fl1,fl2) -> fl1=fl2


type 'a option = None | Some of 'a
                 
let rec lookup key dict =
  match dict with
  | [] -> None
  | (k,v)::t ->
    if k=key
    then Some v
    else lookup key t


type ('a,'b) either = Left of 'a | Right of 'b

type 'a bt = Empty | Node of 'a * 'a bt * 'a bt

let t : int bt =
  Node(12,
       Node(7,Empty,Empty),
       Node(33,
            Node(24,Empty,Empty),
            Empty))

let rec sizet (t:'a bt) : int =
  match t with
  | Empty -> 0
  | Node(d,lt,rt) -> 1 + sizet lt + sizet rt

let rec sumt (t:int bt) : int =
  match t with
  | Empty -> 0
  | Node(d,lt,rt) -> d + sumt lt + sumt rt

let rec height t =
  match t with
  | Empty -> 0
  | Node(_,lt,rt) -> 1 + max (height lt) (height rt)

let rec m (t:'a bt) : 'a bt =
  match t with
  | Empty -> Empty
  | Node(d,lt,rt) -> Node(d,m rt, m lt)

let rec po t =
  match t with
  | Empty -> []
  | Node(d,lt,rt) -> d :: (po lt @ po rt)
                          
let rec mapt (f:'a->'b) (t:'a bt) : 'b bt =
  match t with
  | Empty -> Empty
  | Node(d,lt,rt) -> Node(f d, mapt f lt, mapt f rt)

let rec foldt (f:'a -> 'b -> 'b -> 'b) (a:'b) (t:'a bt) : 'b  =
  match t with
  | Empty -> a
  | Node(d,lt,rt) -> f d (foldt f a lt) (foldt f a rt)


let rec is_leaf t =
  match t with
  | Node(_,Empty,Empty) -> true
  | _ -> false

(* Hint: Use List.map *)

let rec paths_to_leaves t =
  match t with
  | Empty -> []
  | Node(d,Empty,Empty) -> [ [] ]
  | Node(d,lt,rt) ->
   List.map (fun l -> 0::l) (paths_to_leaves lt)
   @
   List.map (fun l -> 1::l) (paths_to_leaves rt)

let rec paths t =
  match t with
  | Empty -> []
  | Node(d,Empty,Empty) -> [ [] ]
  | Node(d,lt,rt) ->
   [] :: List.map (fun l -> 0::l) (paths_to_leaves lt)
   @
   List.map (fun l -> 1::l) (paths_to_leaves rt)


(* Quiz 2 *)
(* 
   One submission per group
   Name of both partners in source code
   Name of other member (the one not submitting) as a canvas comment
*)

(* [prune n t] prunes the tree [t] at level [n].
   If [n] is larger than the height of [t], then it returns [t].
   Also, [prune 0 t] ==> Empty 
*)

let rec prune n t =
  if (n>0) then 
    (match t with
    | Empty -> Empty
    | Node(d,lt,rt) -> Node(d, prune (n-1) lt, prune (n-1) rt))
  else 
    Empty 

(* [perfect t] determines whether [t] is a perfect binary tree
   [t] is perfect if the length of all the
 * paths to all the leaves is the same *)
let perfect t =
  let k = paths_to_leaves t in List.for_all (fun (l : int list) -> List.length l=List.length @@ List.hd @@ k) k
