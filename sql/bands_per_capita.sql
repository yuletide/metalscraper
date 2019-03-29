CREATE TABLE bands_percapita as SELECT *, 
(CASE WHEN eb_gpw.pop_2020 = 0 THEN 
 0
 ELSE
 admin_1_bands_join.bands_count::decimal / eb_gpw.pop_2020
 END) as bands_percapita 
from admin_1_bands_join JOIN eb_gpw USING (id_int)
ORDER BY bands_percapita DESC