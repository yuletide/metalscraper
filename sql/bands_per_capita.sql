CREATE TABLE bands_percapita2 AS
SELECT
	*,
	(CASE WHEN eb_gpw.pop_2020 = 0 THEN 0
		ELSE
			admin_1_bands_join.bands_count ::decimal / eb_gpw.pop_2020
		END) AS bands_percapita
FROM
	admin_1_bands_join
	JOIN eb_gpw_all USING (
		id_int)
ORDER BY
	bands_percapita DESC