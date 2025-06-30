from sqlalchemy import text

drop_views = text("""
DROP MATERIALIZED VIEW IF EXISTS sales_with_costs;
DROP MATERIALIZED VIEW IF EXISTS product_margins;
""")

sales_with_costs_view = text("""
DROP MATERIALIZED VIEW IF EXISTS sales_with_costs;
CREATE MATERIALIZED VIEW sales_with_costs AS
SELECT
    s.*,
    p.purchase_price,
    ROUND((s.sale_quantity * p.purchase_price)::numeric, 2) as total_cost,
    ROUND((s.sale_amount - (s.sale_quantity * p.purchase_price))::numeric, 2) as gross_profit,
    ROUND(((s.sale_amount - (s.sale_quantity * p.purchase_price)) - s.excise_tax)::numeric, 2) as net_profit,
    CASE
        WHEN s.sale_amount > 0 
            THEN ROUND(((s.sale_amount - (s.sale_quantity * p.purchase_price)) / s.sale_amount)::numeric, 2)
            ELSE 0
    END AS margin,
    CASE
        WHEN s.sale_amount > 0 
            THEN ROUND((((s.sale_amount - (s.sale_quantity * p.purchase_price)) - s.excise_tax) / s.sale_amount)::numeric, 2)
            ELSE 0
    END AS net_margin
FROM
    sales s
JOIN purchases p
ON s.inventory_id = p.inventory_id;     
""")

product_margins_view = text("""
DROP MATERIALIZED VIEW IF EXISTS product_margins;
CREATE MATERIALIZED VIEW product_margins AS
SELECT
    s.brand,
    s.vendor_name,
    s.sale_price,
    s.excise_tax,
    p.purchase_price,
    ROUND((s.sale_price - p.purchase_price)::numeric, 2) as gross_profit,
    ROUND(((s.sale_price - p.purchase_price) - (s.excise_tax / s.sale_quantity))::numeric, 2) as net_profit,
    CASE
        WHEN s.sale_price > 0 
            THEN ROUND(((s.sale_price - p.purchase_price) / s.sale_price)::numeric, 2)
        ELSE 0
    END AS margin,
    CASE
        WHEN s.sale_price > 0 
            THEN ROUND((((s.sale_price - p.purchase_price) - (s.excise_tax / s.sale_quantity)) / s.sale_price)::numeric, 2)
        ELSE 0
    END AS net_margin
FROM
    sales s
JOIN purchases p
ON s.inventory_id = p.inventory_id;
""")

__all__ = ["drop_views", "sales_with_costs_view", "product_margins_view"]