open Ast
open Ds


let rec apply_proc f arg =
  match f with
  | ProcVal(id,e,env) ->
     return env >>+
     extend_env id arg >>+
     eval_expr e 
  | _ -> error "Expected a closure!"
and 
  eval_expr : expr -> exp_val ea_result = fun e ->
  match e with
  | Int(n) ->
    return (NumVal n)
  | Var(id) ->
    apply_env id
  | Add(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return (NumVal (n1+n2))
  | Sub(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return (NumVal (n1-n2))
  | Mul(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    return (NumVal (n1*n2))
  | Div(e1,e2) ->
    eval_expr e1 >>=
    int_of_numVal >>= fun n1 ->
    eval_expr e2 >>=
    int_of_numVal >>= fun n2 ->
    if n2==0
    then error "Division by zero"
    else return (NumVal (n1/n2))
  | Let(v,def,body) ->
    eval_expr def >>= 
    extend_env v >>+
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
    return (BoolVal (n = 0))
  | Pair(e1,e2) ->
    eval_expr e1 >>= fun ev1 ->
    eval_expr e2 >>= fun ev2 ->
    return (PairVal(ev1,ev2))
  | Fst(e) ->
    eval_expr e >>=
    pair_of_pairVal >>= fun p ->
    return (fst p) 
  | Snd(e) ->
    eval_expr e >>=
    pair_of_pairVal >>= fun p ->
    return (snd p)    
  | Proc(id,body) ->
    lookup_env >>= fun env ->
    return (ProcVal(id,body,env))           
  | App(e1,e2) ->
    eval_expr e1 >>= fun f ->
    eval_expr e2 >>= fun arg ->
    apply_proc f arg
  | Letrec(id,par,e1,e2) ->
    extend_env_rec id par e1 >>+
    eval_expr e2
  | EmptyTree -> return @@ TreeVal Empty
  | Node(e1,lte,rte) ->
    eval_expr e1 >>= fun data ->
    eval_expr lte >>=
    tree_of_treeVal >>= fun lt -> 
    eval_expr rte >>=
    tree_of_treeVal >>= fun rt -> 
    return @@ TreeVal (Node(data,lt,rt))
  | CaseT(target,emptycase,id1,id2,id3,nodecase) ->
    eval_expr target >>= 
    tree_of_treeVal >>= fun v1 ->
    (match v1 with
        | Empty -> eval_expr emptycase
        | Node(v,ltree,rtree) ->
          extend_env id1 v >>+
          extend_env id2 (TreeVal ltree) >>+
          extend_env id3 (TreeVal rtree) >>+
          eval_expr nodecase)
  | Debug(_e) ->
    string_of_env >>= fun str ->
    print_endline str; 
    error "Debug called"
  | _ -> error "Not implemented yet!"

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
let interp (s:string) : exp_val result =
  let c = s |> parse |> eval_expr
  in run c




