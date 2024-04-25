WITH min_max_quants(cust, min_q, max_q, avg_q) AS (
	SELECT cust, MIN(quant), MAX(quant), AVG(quant)
	FROM sales GROUP BY cust
), min_data(cust, min_prod, min_date, min_st) AS (
	SELECT Q.cust, S.prod, S.date, S.state FROM
	sales S, min_max_quants Q WHERE 
	S.cust = Q.cust AND S.quant = Q.min_q
), max_data(cust, max_prod, max_date, max_st) AS (
	SELECT Q.cust, S.prod, S.date, S.state FROM
	sales S, min_max_quants Q WHERE 
	S.cust = Q.cust AND S.quant = Q.max_q
)
SELECT Q.cust as customer, Q.min_q, N.min_prod, N.min_date, N.min_st,
Q.max_q, X.max_prod, X.max_date, X.max_st, Q.avg_q FROM
min_max_quants Q, min_data N, max_data X WHERE 
Q.cust = N.cust and Q.cust = X.cust and N.cust = X.cust