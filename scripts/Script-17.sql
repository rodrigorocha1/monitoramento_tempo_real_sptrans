SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/routes.txt', 
delim=',', 
header=True);

SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/trips.txt', 
delim=',', 
header=True);

SELECT *
from read_csv_auto(
'/home/rodrigo/Documentos/projetos/monitoramento_tempo_real_sptrans/dados/rrrochaa_gtfs/trips.txt', 
delim=',', 
header=True);