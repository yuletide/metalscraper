SELECT
	z0_admin_1.id,
	z0_admin_1.name,
	z0_admin_1.area_sqkm,
	MIN(adminpop. "NAME1") AS gpw_name1,
	COUNT(adminpop. "NAME1") AS gpw_names1_count,
	array_agg(adminpop. "NAME1") AS gpw_names1,
	array_agg(adminpop. "NAME2") AS gpw_names2,
	SUM(adminpop. "TOTAL_A_KM") AS TOTAL_A_KM,
	SUM(adminpop. "UN_2015_E") AS POP_2015,
	SUM(adminpop. "UN_2020_E") AS POP_2020
FROM (z0_admin_1
	RIGHT JOIN gpw_points_oceania AS adminpop ON ST_CONTAINS(z0_admin_1.geom, ST_SetSRID (ST_Point (adminpop. "INSIDE_X", adminpop. "INSIDE_Y"), 4326)))
GROUP BY
	z0_admin_1.id,
	z0_admin_1.name,
	z0_admin_1.area_sqkm
ORDER BY
	gpw_name1 ASC