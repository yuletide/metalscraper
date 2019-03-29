CREATE TABLE bands_percapita2 as 

-- first join bands to a1
WITH a1_bands as (
	SELECT a1.id_int, a1.name, count(bands.geom) as bands_count
	FROM (z0_admin_1 a1 LEFT JOIN swdata bands 
		  ON ST_CONTAINS(a1.geom, bands.geom))
	GROUP BY a1.id_int, a1.name
)

-- then join population and calculate percapita
SELECT *, (
	CASE WHEN eb_gpw.pop_2020 = 0 THEN 0
	ELSE a1_bands.bands_count::decimal / eb_gpw.pop_2020
	END) as bands_percapita 
	FROM a1_bands JOIN eb_gpw_all USING (id_int)
ORDER BY bands_percapita DESC