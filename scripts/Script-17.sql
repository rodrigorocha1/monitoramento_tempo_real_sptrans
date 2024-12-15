
CREATE  TABLE rotas as 
SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/routes.txt', 
delim=',', 
header=True);

CREATE table viagens as 
SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/trips.txt', 
delim=',', 
header=True);

CREATE  table trajetos as 
SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/shapes.txt', 
delim=',', 
header=True);

SELECT shape_pt_lat lat,
	shape_pt_lon lon
FROM trajetos
where shape_id in ();

SELECT shape_id
FROM viagens
WHERE  route_id = ;

SELECT 
	r.route_id route_id,
	r.route_long_name  route_long_name,
	r.route_color as route_color,
	r.route_text_color as route_text_color
from rotas r
where route_id = '1012-10';


SELECT r.route_id, 
	r.route_long_name
FROM rotas r
inner join viagens v on v.route_id = r.route_id
INNER JOIN trajetos t on t.shape_id = v.shape_id;


