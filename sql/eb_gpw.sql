CREATE TABLE eb_gpw as SELECT eb.id_int, MIN(adminpop.NAME1) as gpw_name1, COUNT(adminpop.NAME1) as gpw_names1_count, array_agg(adminpop.NAME1) as gpw_names1, array_agg(adminpop.NAME2) as gpw_names2, SUM(adminpop.TOTAL_A_KM) as TOTAL_A_KM, SUM(adminpop.UN_2015_E) as POP_2015, SUM(adminpop.UN_2020_E) as POP_2020
FROM (z0_admin_1 eb JOIN gpw_points_global adminpop ON 
ST_CONTAINS(eb.geom, ST_SetSRID(ST_Point(adminpop.INSIDE_X, adminpop.INSIDE_Y),4326)))
GROUP BY eb.id_int, eb.area_sqkm