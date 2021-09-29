# graf4geo
Progetto personale per usare PostgreSQL+Grafana per monitoraggi a lungo termine in ambito geofisico, geologico e ambientale

## Comandi per la configurazione del DB Postgres

1. Creare l'utente *grafana* sia sul DB che come utente di sistema:
	'''
	sudo -iu postgres
	createuser --interactive (creare utente grafana)
	logout
	sudo adduser grafana
	sudo -iu postgres
	createdb grafana
	logout
	sudo -u postgres psql
	GRANT pg_read_server_files TO grafana;
	ALTER ROLE grafana SET PASSWORD 'grafana';
	\q
	'''
2. Creare dentro il DB grafana la tabella (table) *data*, attraverso i comandi listati in table.sql:
	'sudo -u grafana psql -f table.sql'
3. Ingestione iniziale dei dati da sorgente CSV nella tabella *data*, sempre con utente grafana:
	'sudo -u grafana psql -c "COPY data FROM '/home/valerio/Works/Grafana/all.csv' DELIMITER ',';"'
4. Controllare che i dati siano correttamente caricati nel DB
	'sudo -u grafana psql -c "SELECT * FROM data;"'

4. Per connettersi al DB PostGres da remoto:
	1. Modificare il file postgresql.conf sostituendo alla riga:
	   ' #listen_addresses='localhost''
	   la riga:
	   'listen_addresses='*''
	2. Aggiungere una riga al file pg_hba.conf:
	    host  all  all 0.0.0.0/0 md5
