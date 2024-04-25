WITH njnyct_maxes(cust, prod, state, state_max) AS (
	SELECT cust, prod, sales.state, MAX(quant) FROM
	sales GROUP BY cust, prod, sales.state HAVING sales.state = 'NJ' OR sales.state = 'NY' OR sales.state = 'CT'
), njnyct_maxdates(cust, prod, state, max_date) AS (
	SELECT S.cust, S.prod, S.state, S.date FROM sales S, njnyct_maxes MA
	WHERE S.quant = MA.state_max AND S.cust = MA.cust AND S.prod = MA.prod
	AND S.state = MA.state
), njnyct_maxdata(cust, prod, state, state_max, max_date) AS (
	SELECT * FROM 
	njnyct_maxes NATURAL JOIN njnyct_maxdates
)
SELECT NJ.cust AS customer, NJ.prod AS product, NJ.state_max AS nj_max, NJ.max_date AS nj_date, NY.state_max AS ny_max, 
NY.max_date AS ny_date, CT.state_max AS ct_max, CT.max_date AS ct_date FROM
njnyct_maxdata NJ, njnyct_maxdata NY, njnyct_maxdata CT WHERE 
NJ.cust = NY.cust AND NJ.cust = CT.cust AND NY.cust = CT.cust AND
NY.prod = NY.prod AND NJ.prod = CT.prod AND NY.prod = CT.prod AND
NJ.state = 'NJ' AND NY.state = 'NY' AND CT.state = 'CT'
