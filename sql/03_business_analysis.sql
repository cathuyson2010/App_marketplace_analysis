USE app_marketplace;
-- Snapshot metadata: installs are lower-bound buckets, not revenue or growth.
-- Q1: Supply and observed demand by category.
SELECT category, COUNT(*) AS app_count, COUNT(rating) AS rated_apps,
 ROUND(AVG(rating),3) AS avg_rating, SUM(installs) AS total_installs,
 ROUND(AVG(installs),0) AS mean_installs
FROM apps GROUP BY category ORDER BY total_installs DESC;

-- Q2: Ratings with a minimum sample of 50 rated apps (analyst threshold).
SELECT category, COUNT(rating) AS rated_apps, ROUND(AVG(rating),3) AS avg_rating
FROM apps GROUP BY category HAVING COUNT(rating)>=50 ORDER BY avg_rating DESC;

-- Q3: Free versus Paid across the sample.
SELECT app_type, COUNT(*) AS app_count, ROUND(AVG(rating),3) AS avg_rating,
 ROUND(AVG(installs),0) AS mean_installs, ROUND(AVG(price),2) AS mean_price
FROM apps GROUP BY app_type;

-- Q4: Free versus Paid in GAME.
SELECT app_type, COUNT(*) AS app_count, ROUND(AVG(rating),3) AS avg_rating,
 SUM(installs) AS installs, ROUND(AVG(installs),0) AS mean_installs,
 ROUND(AVG(price),2) AS mean_price
FROM apps WHERE category='GAME' GROUP BY app_type;

-- Q5: Paid categories (minimum 5 apps; not evidence of profitability).
SELECT category,COUNT(*) AS paid_apps,ROUND(AVG(price),2) AS mean_price,
 ROUND(AVG(rating),3) AS avg_rating,ROUND(AVG(installs),0) AS mean_installs
FROM apps WHERE app_type='Paid'
GROUP BY category HAVING COUNT(*)>=5 ORDER BY mean_installs DESC;

-- Q6: GAME primary genre; first semicolon-delimited genre only.
SELECT SUBSTRING_INDEX(genres,';',1) AS primary_genre,COUNT(*) AS games,
 ROUND(AVG(rating),3) AS avg_rating,SUM(installs) AS total_installs
FROM apps WHERE category='GAME' GROUP BY primary_genre ORDER BY total_installs DESC;

-- Q7: Exactly three apps per category, deterministic tie break.
WITH ranked AS (
 SELECT app_name,category,rating,installs,
 ROW_NUMBER() OVER(PARTITION BY category ORDER BY installs DESC,reviews DESC,app_id) AS position
 FROM apps)
SELECT * FROM ranked WHERE position<=3 ORDER BY category,position;

-- Q8: Category medians include unrated apps if present.
WITH ordered AS (
 SELECT category,installs,ROW_NUMBER() OVER(PARTITION BY category ORDER BY installs,app_id) AS rn,
 COUNT(*) OVER(PARTITION BY category) AS n FROM apps WHERE installs IS NOT NULL)
SELECT category,AVG(installs) AS median_installs FROM ordered
WHERE rn IN (FLOOR((n+1)/2),FLOOR((n+2)/2))
GROUP BY category ORDER BY median_installs DESC;

-- Q9: Share of category installs held by its top three apps.
WITH ranked AS (
 SELECT category,installs,
 ROW_NUMBER() OVER(PARTITION BY category ORDER BY installs DESC,app_id) AS rn FROM apps)
SELECT category,SUM(installs) AS total_installs,
 ROUND(100.0*SUM(CASE WHEN rn<=3 THEN installs ELSE 0 END)/NULLIF(SUM(installs),0),2) AS top3_share_pct
FROM ranked GROUP BY category ORDER BY top3_share_pct DESC;

-- Q10: Above-category-average ratings using a correlated subquery.
SELECT a.app_name,a.category,a.rating,a.installs FROM apps a
WHERE a.rating>(SELECT AVG(b.rating) FROM apps b WHERE b.category=a.category)
ORDER BY a.category,a.rating DESC,a.app_name;

-- Q11: Adoption buckets are analyst-defined, not measured success probabilities.
SELECT CASE WHEN installs IS NULL THEN 'Unknown'
 WHEN installs>=100000000 THEN '100M+' WHEN installs>=10000000 THEN '10M-100M'
 WHEN installs>=1000000 THEN '1M-10M' ELSE 'Below 1M' END AS install_band,
 COUNT(*) AS app_count,ROUND(AVG(rating),3) AS avg_rating
FROM apps GROUP BY install_band;

-- Q12: JOIN each app to a category benchmark without inventing a second dataset.
WITH benchmarks AS (
 SELECT category,AVG(rating) AS category_rating,AVG(installs) AS category_installs
 FROM apps GROUP BY category)
SELECT a.app_name,a.category,a.rating,a.installs,
 ROUND(b.category_rating,3) AS category_rating,ROUND(b.category_installs,0) AS category_installs
FROM apps a INNER JOIN benchmarks b ON a.category=b.category
WHERE a.rating>b.category_rating AND a.installs<b.category_installs
ORDER BY a.category,a.rating DESC,a.app_name;
