WITH qrtr_avgs(qrtr, cust, prod, q_avg) AS (
	SELECT (sales.month - 1) / 3 + 1 as qrtr, cust, prod, AVG(quant) FROM 
	sales GROUP BY qrtr, cust, prod
), prod_tots(customer, product, average, total, count) AS (
	SELECT cust, prod, AVG(quant), SUM(quant), COUNT(quant) FROM 
	sales GROUP BY cust, prod
)
SELECT PT.customer, PT.product, Q1.q_avg as q1_avg, Q2.q_avg AS q2_avg,
Q3.q_avg AS q3_avg, Q4.q_avg as q4_avg, PT.average, PT.total, PT.count
FROM prod_tots PT, qrtr_avgs Q1, qrtr_avgs Q2, qrtr_avgs Q3, qrtr_avgs Q4
WHERE PT.customer = Q1.cust and PT.product = Q1.prod AND Q1.qrtr = 1
AND PT.customer = Q2.cust and PT.product = Q2.prod AND Q2.qrtr = 2
AND PT.customer = Q3.cust and PT.product = Q3.prod AND Q3.qrtr = 3
AND PT.customer = Q4.cust and PT.product = Q4.prod AND Q4.qrtr = 4


