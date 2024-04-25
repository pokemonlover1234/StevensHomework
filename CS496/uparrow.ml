#require "bignum.bigint"

let big n = Big_int.big_int_of_int n;;

let rec uparrow n = 
  match n with
  | 0 -> let mult a b = Big_int.mult_big_int a b in mult
  | 1 -> let expon a b = Big_int.power_big_int_positive_big_int a b in expon
  | m when n > 1 -> (
    let rec upexpo oa ob a b = (
      if (Big_int.eq_big_int b Big_int.unit_big_int) then a else 
        (upexpo oa ob (uparrow (n-1) oa a) (Big_int.pred_big_int b))
    ) in (let upexp a b = (
        if (Big_int.eq_big_int b Big_int.unit_big_int) then a else
          (upexpo a b (uparrow (n-1) a a) (Big_int.pred_big_int b))
      ) in upexp
    )
  )
  | m when n < 0 -> failwith "uparrow does not work with negative inputs"