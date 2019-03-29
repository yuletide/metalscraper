CREATE TABLE admin_1_bands_lookup as SELECT z0_admin_1.id, z0_admin_1.name, count(bands.wkb_geometry) as BANDS_COUNT
FROM (z0_admin_1 LEFT JOIN bands ON 
ST_CONTAINS(z0_admin_1.geom, bands.wkb_geometry))
GROUP BY z0_admin_1.id, z0_admin_1.name