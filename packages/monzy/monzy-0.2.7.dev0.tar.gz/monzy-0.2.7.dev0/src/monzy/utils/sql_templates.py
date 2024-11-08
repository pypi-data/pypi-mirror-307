add_id = """
UPDATE {table}
SET lunch_money_id = {lunch_money_id}
WHERE id IN ('{external_id}')
"""

get_id = """
SELECT lunch_money_id
FROM {table} x
WHERE x.id IN ('{external_id}')
"""

delete = """
DELETE FROM {table} x
WHERE x.id IN ({data})
"""

exists = """
SELECT
"id",
"date",
"timestamp",
"description",
"amount",
"category",
"notes",
"tags",
"source",
"lunch_money_id"
FROM {table}
"""

exists_pots = """
SELECT
"id",
"name",
"style",
"balance",
"currency",
"deleted"
FROM {table} x
"""

past_week_transactions_agg = """
SELECT a.category,
sum(a.count) AS frequency,
sum(a.amount) AS total_amount
FROM (
SELECT count(*),
category,
amount
FROM {table}
WHERE date < current_date
AND date > (current_date - interval '7 day')
GROUP BY date,
category,
amount
ORDER BY date desc
) a
GROUP BY a.category
ORDER BY sum(a.amount) DESC
"""
