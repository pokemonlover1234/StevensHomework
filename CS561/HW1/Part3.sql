WITH prod_sums(prod, mon, tot_quant) AS (
	SELECT sales.prod, sales.month, SUM(sales.quant) 
	FROM sales GROUP BY sales.prod, sales.month
), month_minmax(prod, min_quant, max_quant) AS (
	SELECT prod, MIN(tot_quant), MAX(tot_quant)
	FROM prod_sums GROUP BY prod
)
SELECT MM.prod as product, MA.mon as most_fav_mo, LE.mon as least_fav_mo 
FROM month_minmax MM, prod_sums LE, prod_sums MA WHERE
MM.prod = LE.prod AND MM.prod = MA.prod and LE.prod = MA.prod 
AND LE.tot_quant = MM.min_quant AND MA.tot_quant = MM.max_quant