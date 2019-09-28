CREATE TABLE
IF NOT EXISTS gpw_nn as
SELECT
	gpw.*, eb.id_int as eb_id, eb.name as eb_name, ST_DISTANCE(geography(gpw.geom_inside), geography(eb.geom)) as distance
FROM
	gpw_points gpw
CROSS JOIN LATERAL
	(
SELECT id_int, name, geom
FROM z0_admin_1
ORDER BY 
		geom
<-> gpw.geom_inside
	LIMIT 1) as eb;

with
	gpw
	as
	(
		SELECT eb_id, SUM("TOTAL_A_KM") as gpw_area
		from gpw_nn
		WHERE distance<100
		GROUP BY eb_id
	)

select gpw.*, eb.area_sqkm, eb.name
from
	gpw JOIN z0_admin_1v2 eb ON gpw.eb_id=eb.id_int
