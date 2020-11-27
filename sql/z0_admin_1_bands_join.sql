CREATE TABLE admin_1_bands_lookup AS
SELECT
	z0_admin_1.id_int,
	z0_admin_1.name,
	count(
		bands.wkb_geometry) AS BANDS_COUNT
FROM (
	z0_admin_1
	LEFT JOIN swdata bands ON ST_CONTAINS(z0_admin_1.geom, bands.wkb_geometry))
GROUP BY
	z0_admin_1.id_int,
	z0_admin_1.name