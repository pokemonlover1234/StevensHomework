open OUnit2
open Recht.Interp
open Recht.Ds

(* A few test cases *)
let tests_let = [
  "int"  >:: (fun _ -> assert_equal (Ok (NumVal 22)) (interp "22"));
  "add"  >:: (fun _ -> assert_equal (Ok (NumVal 22)) (interp "11+11"));
  "adds" >:: (fun _ -> assert_equal (Ok (NumVal 22)) (interp "(10+1)+(5+6)"));
  "let"  >:: (fun _ -> assert_equal (Ok (NumVal 22)) (interp "let x=22 in x"));
  "lets" >:: (fun _ -> assert_equal (Ok (NumVal 22)) (interp "let x = 0 in let x = 22 in x"));
]


let tests_proc = [
  "int"  >:: (fun _ -> assert_equal (Ok (NumVal 3))
                 (interp "(proc (x) { x+1 } 2)"))
]

let tests_rec = [
  "int"  >:: (fun _ -> assert_equal (Ok (NumVal 120))
                 (interp "letrec f(x) = if zero?(x) then 1 else x*(f (x-1))
in (f 5)"))
]


let tests_recht = [
  "table1"  >:: (fun _ -> assert_equal (Ok (TableVal []))
                 (interp "emptytable"))
  ;
  "table2"  >:: (fun _ -> assert_equal (Ok
 (TableVal
   [(NumVal 0, NumVal 1234); (NumVal 1, NumVal 5678); (NumVal 2, NumVal 9101);
    (NumVal 3, NumVal 1121)]))
                 (interp "insert(0, 1234, insert(1, 5678, insert(2,9101, insert(3, 1121, emptytable))))"))
  ;
    "table3"  >:: (fun _ -> assert_equal (Ok (NumVal 9101))
                      (interp
                         "lookup(2, insert(0, 1234, insert(1, 5678,
  insert(2,9101, insert(3, 1121, emptytable)))))"))
  ;
    "table4"  >:: (fun _ -> assert_equal (Ok
 (TableVal
   [(NumVal 0, NumVal 1234); (NumVal 1, NumVal 5678); (NumVal 3, NumVal 1121)]))
                      (interp
                         "remove(2, insert(0, 1234, insert(1, 5678,
  insert(2,9101, insert(3, 1121, emptytable)))))"))
  ;
    "table5"  >:: (fun _ -> assert_equal (Ok (NumVal 3))
                      (interp
                          "size(remove(2, insert(0, 1234, insert(1,
  5678, insert(2,9101, insert(3, 1121, emptytable))))))"))
  ;
     "table6"  >:: (fun _ -> assert_equal ( Ok (BoolVal false))
                      (interp
                           "empty?(remove(2, insert(0, 1234, insert(1, 5678, insert(2,9101, insert(3, 1121, emptytable))))))"))
]

let _ = run_test_tt_main ("suite" >::: (tests_let @ tests_proc
                                        @ tests_rec @ tests_recht))
