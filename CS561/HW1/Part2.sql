WITH sales_sums(qrtr, date, total) AS (
	SELECT (sales.month - 1) / 3 + 1 as QRTR, sales.date, SUM(quant) FROM
	sales GROUP BY qrtr, sales.date
), minmaxes(qrtr, min_tot, max_tot) AS (
	SELECT qrtr, MIN(total), MAX(total) FROM sales_sums GROUP BY qrtr
)
SELECT MM.qrtr, MO.date AS most_profit_date, MO.total AS most_profit_total_q, 
LE.date AS least_profit_day, LE.total AS least_profit_total_q FROM 
sales_sums MO, sales_sums LE, minmaxes MM WHERE MO.total = MM.max_tot AND 
LE.total = MM.min_tot AND MO.qrtr = LE.qrtr AND MO.qrtr = MM.qrtr and LE.qrtr = MM.qrtr
	