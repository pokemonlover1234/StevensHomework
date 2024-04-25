(* 

   Quiz4A
   
    Name1: Aidan Fischer
    Name2: N/A

  I pledge my honor that I have abided by the Stevens Honor System.
*)

open Ast
open Ds
             

let rec apply_proc : exp_val -> exp_val -> exp_val ea_result =
  fun f a ->
  match f with
  | ProcVal (id,body,env) ->
    return env >>+
    extend_env id a >>+
    eval_expr body
  | _ -> error "apply_proc: Not a procVal"
and
 eval_expr : expr -> exp_val ea_result = fun e ->
  match e with
  | Int(n) ->
    return @@ NumVal n
  | Var(id) ->
    apply_env id
  | Add(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return @@ NumVal (n1+n2)
  | Sub(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return @@ NumVal (n1-n2)
  | Mul(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return @@ NumVal (n1*n2)
  | Div(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    if n2==0
    then error "Division by zero"
    else return @@ NumVal (n1/n2)
  | Let(id,def,body) ->
    eval_expr def >>= 
    extend_env id >>+
    eval_expr body 
  | ITE(e1,e2,e3) ->
    eval_expr e1 >>=
    bool_of_boolVal >>= fun b ->
    if b 
    then eval_expr e2
    else eval_expr e3
  | IsZero(e) ->
    eval_expr e >>=
    int_of_numVal >>= fun n ->
    return @@ BoolVal (n = 0)
  | Proc(id,e)  ->
    lookup_env >>= fun en ->
    return (ProcVal(id,e,en))
  | App(e1,e2)  -> 
    eval_expr e1 >>= fun v1 ->
    eval_expr e2 >>= fun v2 ->
    apply_proc v1 v2 
  | Abs(e1)      ->
    eval_expr e1 >>= int_of_numVal >>= fun v ->
    return @@ NumVal(abs v)
  | Cons(e1, e2) ->
    eval_expr e1 >>= fun v ->
    eval_expr e2 >>=
    list_of_listVal >>= fun l ->
    return @@ ListVal(v :: l)
  | Hd(e1) ->
    eval_expr e1 >>= list_of_listVal >>= fun l ->
    if (List.length l = 0) then error "hd expects non-empty list" else return @@ List.hd l
  | Tl(e1) ->
    eval_expr e1 >>= list_of_listVal >>= fun l ->
    if (List.length l = 0) then error "tl expects non-empty list" else return @@ ListVal(List.tl l)
  | Empty(e1) ->
    eval_expr e1 >>= fun v ->
    if(is_listVal v) then
    return v >>= list_of_listVal >>= fun l ->
    return @@ BoolVal(List.length l = 0)
    else
    return v >>= tree_of_treeVal >>= fun t ->
    return @@ BoolVal(t = Empty)
  | EmptyList ->
    return @@ ListVal([])
  | EmptyTree ->
    return @@ TreeVal Empty
  | Node(e1,lte,rte) ->
    eval_expr e1 >>= fun v ->
    eval_expr lte >>= tree_of_treeVal >>= fun lt ->
    eval_expr rte >>= tree_of_treeVal >>= fun rt ->
    return @@ TreeVal(Node(v, lt, rt))
  | CaseT(target,emptycase,id1,id2,id3,nodecase) ->
    eval_expr target >>= tree_of_treeVal >>= fun t ->
    match t with
    | Empty -> (
      eval_expr emptycase >>= fun v ->
      return v)
    | Node(a, l, r) -> (
      return a >>= extend_env id1 >>+
      (return @@ TreeVal l >>= extend_env id2 >>+
      (return @@ TreeVal r >>= extend_env id3 >>+
      eval_expr nodecase >>= fun v ->
      return v))
    )
    
and
  eval_prog (AProg e) = eval_expr e

(***********************************************************************)
(* Everything above this is essentially the same as we saw in lecture. *)
(***********************************************************************)

(* Parse a string into an ast *)

let parse s =
  let lexbuf = Lexing.from_string s in
  let ast = Parser.prog Lexer.read lexbuf in
  ast

let lexer s =
  let lexbuf = Lexing.from_string s
  in Lexer.read lexbuf 


(* Interpret an expression *)
let interp (e:string) : exp_val result =
  let c = e |> parse |> eval_prog
  in run c



