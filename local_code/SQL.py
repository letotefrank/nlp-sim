'''
1.product_base.csv

SELECT DISTINCT ps.`product_id`,
                ps.`season_id`,
                p.`type`,
                c.`ancestry`,
                c.`name`
FROM   products p,
       product_seasons ps,
       product_categories pc,
       categories c
WHERE  p.id = ps.product_id
and p.id = pc.product_id
and pc.`category_id` = c.id
   AND ps.`primary` = 1
ORDER  BY ps.product_id ;


2.customer_base.csv

SELECT s.`customer_id`,
       s.`shape`,
       ( Year(Now()) - Year(s.`birthday`) - 1 ) + (
       Date_format(s.`birthday`, '%m%d') <= Date_format(Now(), '%m%d') ) AS age,
       s.`occupation`,
       s.`marital_status`,
       cc.`city`
FROM   `styles` s,
       customer_cities cc
WHERE  s.`customer_id` = cc.`customer_id`
ORDER  BY s.`customer_id`;


3.heat_rank_data.csv
    fashion-rec.fit_model.py

'''
