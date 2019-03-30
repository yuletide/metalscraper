CREATE TABLE gpw_nn as
SELECT
	gpw.*, eb.id_int as eb_id, eb.name as eb_name, ST_DISTANCE(geography(gpw.geom), geography(eb.geom)) as distance
FROM
	gpw_points_africa gpw
CROSS JOIN LATERAL
	(SELECT id_int, name, geom
	FROM z0_admin_1 
	ORDER BY 
		geom <-> gpw.geom 
	LIMIT 1) as eb

with gpw as (
SELECT eb_id, SUM("TOTAL_A_KM") as gpw_area from gpw_nn WHERE distance<5
GROUP BY eb_id)

select gpw.*, eb.area_sqkm, eb.name from
gpw JOIN z0_admin_1 eb ON gpw.eb_id=eb.id_int
