ALTER TABLE gpw_points_africa
	ADD COLUMN geom_inside GEOMETRY(POINT, 4326);
	
UPDATE gpw_points_africa
SET geom_inside = ST_SetSRID(ST_Point("INSIDE_X", "INSIDE_Y"),4326);

CREATE INDEX gpw_points_africa_inside_idx
ON gpw_points_africa
USING GIST(geom_inside);