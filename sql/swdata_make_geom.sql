-- alter table swdata drop column geom;
ALTER TABLE swdata 
	ADD COLUMN
IF NOT EXISTS geom GEOMETRY
(POINT, 4326);

UPDATE
	swdata
SET
	geom = ST_SetSRID (ST_GeomFromGeoJson(replace(replace(geo_geom, '''', '"'), 'u', '')::json),
		4326)
WHERE
	geo_geom IS NOT NULL