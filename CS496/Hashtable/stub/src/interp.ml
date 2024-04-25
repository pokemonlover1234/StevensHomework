open Ast
open Ds


let rec apply_proc : exp_val -> exp_val -> exp_val ea_result =
  fun f a ->
  match f with
  |  ProcVal (id,body,env) ->
    return env >>+
    extend_env id a >>+
    eval_expr body
  | _ -> error "apply_proc: Not a procVal"
and
  eval_expr : expr -> exp_val ea_result = fun e ->
  match e with
  | Int(n) -> return (NumVal n)
  | Var(id) -> apply_env id
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
  | Proc(id,e)  ->
    lookup_env >>= fun en ->
    return (ProcVal(id,e,en))
  | App(e1,e2)  -> 
    eval_expr e1 >>= fun v1 ->
    eval_expr e2 >>= fun v2 ->
    apply_proc v1 v2
  | Letrec(id,par,e1,e2) ->
    extend_env_rec id par e1 >>+
    eval_expr e2
  | EmptyTable ->
    return @@ TableVal []
  | Insert(e1,e2,e3) ->
    eval_expr e1 >>= fun ind -> 
    eval_expr e2 >>= fun value ->
    eval_expr e3 >>= table_of_tableVal >>= fun tbl ->
    (match ind with 
    | ProcVal(_,_,_) -> error "Insert: Key cannot be ProcVal"
    | _ -> return @@ TableVal ((ind, value) :: tbl))
  | Lookup(e1,e2) ->
    eval_expr e1 >>= fun ind ->
    eval_expr e2 >>= table_of_tableVal >>= fun tbl ->
    (let rec lookup_helper tb = 
      match tb with 
      | [] -> error "Lookup: Key not found."
      | (i,v)::t -> if (i = ind) then return v else lookup_helper t
    in lookup_helper tbl)
  | Remove(e1,e2) ->
    eval_expr e1 >>= fun ind ->
      eval_expr e2 >>= table_of_tableVal >>= fun tbl ->
      (let rec remv_helper tb = 
        match tb with 
        | [] -> []
        | (i,v)::t -> if (i = ind) then remv_helper t else (i,v) :: remv_helper t
      in let res = remv_helper tbl in
      if (List.length tbl = List.length res) then error "Remove: Key not found."
      else return @@ TableVal res)
  | IsEmpty(e) ->
    eval_expr e >>= table_of_tableVal >>= fun tbl ->
    return @@ BoolVal (List.length tbl = 0)
  | Size(e) ->
    eval_expr e >>= table_of_tableVal >>= fun tbl ->
    (let rec sz_helper tb = 
      match tb with 
      | [] -> 0
      | _::t -> 1 + sz_helper t
    in return @@ NumVal (sz_helper tbl))
 | Debug(_e) ->
    string_of_env >>= fun str ->
    print_endline str; 
    error "Debug called"
  | _ -> error "Not implemented yet!"

(** [parse s] parses string [s] into an ast *)
let parse (s:string) : expr =
  let lexbuf = Lexing.from_string s in
  let ast = Parser.prog Lexer.read lexbuf in
  ast


(** [interp s] parses [s] and then evaluates it *)
let interp (s:string) : exp_val result =
  let c = s |> parse |> eval_expr
  in run c


