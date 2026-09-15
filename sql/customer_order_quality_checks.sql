-- SQL Data Quality & Reconciliation Checks
-- Portfolio examples for validating an orders dataset.

-- 1. Find duplicate order IDs
SELECT order_id, COUNT(*) AS record_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. Find required fields that are missing
SELECT *
FROM orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR order_date IS NULL;

-- 3. Detect invalid monetary values
SELECT order_id, order_total
FROM orders
WHERE order_total < 0;

-- 4. Reconcile order totals against line-item totals
SELECT
    o.order_id,
    o.order_total AS header_total,
    SUM(oi.quantity * oi.unit_price) AS calculated_total,
    o.order_total - SUM(oi.quantity * oi.unit_price) AS difference
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.order_total
HAVING ABS(o.order_total - SUM(oi.quantity * oi.unit_price)) > 0.01;

-- 5. Daily data-quality summary
SELECT
    CAST(order_date AS DATE) AS order_day,
    COUNT(*) AS total_orders,
    COUNT(DISTINCT order_id) AS unique_orders,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_ids,
    SUM(CASE WHEN order_total < 0 THEN 1 ELSE 0 END) AS invalid_totals
FROM orders
GROUP BY CAST(order_date AS DATE)
ORDER BY order_day DESC;
