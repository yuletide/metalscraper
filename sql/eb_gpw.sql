CREATE TABLE IF NOT EXISTS eb_gpw AS
	SELECT
		eb.id_int,
		MIN(adminpop.NAME1) AS gpw_name1,
		COUNT(adminpop.NAME1) AS gpw_names1_count,
		array_agg(adminpop.NAME1) AS gpw_names1,
		array_agg(adminpop.NAME2) AS gpw_names2,
		SUM(adminpop.TOTAL_A_KM) AS TOTAL_A_KM,
		SUM(adminpop.UN_2015_E) AS POP_2015,
		SUM(adminpop.UN_2020_E) AS POP_2020
	FROM (z0_admin_1 eb JOIN gpw_points_global adminpop ON
		ST_CONTAINS(eb.geom, ST_SetSRID(ST_Point(adminpop.INSIDE_X, adminpop.INSIDE_Y),4326)))
		GROUP BY eb.id_int, eb.area_sqkm;

SELECT
	gpw.*,
	eb.id_int AS eb_id,
	eb.name AS eb_name,
	ST_DISTANCE(geography (gpw.geom), geography (eb.geom)) AS distance
FROM
	gpw_points_africa gpw
	CROSS JOIN LATERAL (
		SELECT
			id_int,
			name,
			geom
		FROM
			z0_admin_1
		ORDER BY
			geom <-> gpw.geom
		LIMIT 1) AS eb