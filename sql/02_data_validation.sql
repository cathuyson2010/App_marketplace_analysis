USE app_marketplace;
-- Expected for the current cleaned CSV: 8196 apps, 33 categories.
SELECT COUNT(*) AS total_apps,COUNT(DISTINCT category) AS categories,
 COUNT(DISTINCT BINARY app_name) AS unique_names FROM apps;
-- Expected: 912 GAME apps; 13878762717 installs.
SELECT COUNT(*) AS game_apps,SUM(installs) AS game_installs
FROM apps WHERE category='GAME';
-- All invalid counts should be zero.
SELECT SUM(rating<0 OR rating>5) AS invalid_ratings,
 SUM(installs<0) AS negative_installs,SUM(reviews<0) AS negative_reviews,
 SUM(price<0) AS negative_prices,
 SUM(category IS NULL OR TRIM(category)='') AS missing_categories
FROM apps;
SELECT SUM(rating IS NULL) AS missing_ratings,
 SUM(installs IS NULL) AS missing_installs FROM apps;
SELECT category,COUNT(*) AS app_count,SUM(installs) AS installs
FROM apps GROUP BY category ORDER BY category;
SELECT app_name,COUNT(*) AS duplicates FROM apps
GROUP BY BINARY app_name,app_name HAVING COUNT(*)>1;
