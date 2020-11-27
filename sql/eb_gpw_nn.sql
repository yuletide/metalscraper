CREATE TABLE IF NOT EXISTS gpw_nn AS
	SELECT
		gpw.*,
		eb.id_int AS eb_id,
		eb.name AS eb_name,
		ST_DISTANCE(geography (gpw.geom_inside), geography (eb.geom)) AS distance
	FROM
		gpw_points gpw
	CROSS JOIN LATERAL (
	SELECT
		id_int,
		name,
		geom
	FROM
		z0_admin_1
	ORDER BY
		geom <-> gpw.geom_inside
	LIMIT 1) AS eb;

WITH gpw AS (
	SELECT
		eb_id,
		SUM("TOTAL_A_KM") AS gpw_area
	FROM
		gpw_nn
	WHERE
		distance < 100
	GROUP BY
		eb_id
)
SELECT
	gpw.*,
	eb.area_sqkm,
	eb.name
FROM
	gpw
	JOIN z0_admin_1v2 eb ON gpw.eb_id = eb.id_int