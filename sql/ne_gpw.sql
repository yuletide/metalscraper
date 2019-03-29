-- CREATE TABLE ne_gpw
-- AS
SELECT
	a1.ne_id,
	MIN(adminpop."NAME1") AS gpw_name1,
	COUNT(adminpop."NAME1") AS gpw_names1_count,
 	array_agg(adminpop."NAME1") AS gpw_names1,
 	SUM(adminpop."TOTAL_A_KM") AS total_a_km,
 	SUM(adminpop."UN_2015_E") AS pop_2015,
	SUM(adminpop."UN_2020_E") AS pop_2020
FROM (ne_admin1 a1
	JOIN gpw_points_oceania adminpop ON ST_CONTAINS (a1.geom,
		ST_SetSRID (ST_Point (adminpop."INSIDE_X",
				adminpop."INSIDE_Y"),
			4326)))
GROUP BY
	a1.ne_id,
	a1.area_sqkm