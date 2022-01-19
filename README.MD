# graf4geo
Progetto personale per usare PostgreSQL+Grafana per monitoraggi a lungo termine in ambito geofisico, geologico e ambientale

## Le premesse: installazione di PostgreSQL (RHEL e derivate)

1. Installare sia il client che il server:

`$ sudo yum install -y postgresql postgresql-contrib postgresql-server`

2. Inizializzare il DB, creando un nuovo cluster:

`$ sudo postgresql-setup initdb`

3. Abilitare il server PostgreSQL all'avvio automatico:

`$ sudo systemctl enable postgresql.service`

4. Avviare il server PostgreSQL:

`$ sudo systemctl start postgresql.service`


## Configurazione del DB Postgres

1. Creare l'utente *grafana* (o dbreader, in caso installazione da pacchetti) sia sul DB che come utente di sistema:
	```
	$ sudo -iu postgres
	$ createuser --interactive (creare utente non amministrativo dbreader)
        $ createdb dbreader (creare DB omonimo all'utente appena creato)
	$ logout
	$ sudo adduser dbreader
	$ sudo -u postgres psql
	> GRANT pg_read_server_files TO dbreader;
	> ALTER ROLE dbreader WITH PASSWORD 'dbreader';
	> \q
	```

2. Creare dentro il DB grafana la tabella (table) *data*, attraverso i comandi listati in table.sql:

	`$ sudo -u grafana psql -f table.sql`
  
	Se ci sono problemi di accesso dell'utente *grafana* (o timeseries) sulla cartella dell'utente attuale, e' un problema
	di ACL, che si risolve dando il comando:
	
	`$ sudo setfacl -m g::rwx /home/grafana`
	
        Corrispondentemente, aggiungere l'utente *grafana* al gruppo dell'utente corrente (o gruppo _users_)


3. Ingestione iniziale dei dati da sorgente CSV nella tabella *data*, sempre con utente grafana:

	`$ sudo -u grafana psql -c "COPY data FROM '/home/valerio/Works/Grafana/all.csv' DELIMITER ',';"`


4. Controllare che i dati siano correttamente caricati nel DB:

	`$ sudo -u grafana psql -c "SELECT * FROM data;"`


4. Per connettersi al DB PostGres da remoto:
	1. Modificare il file postgresql.conf sostituendo alla riga:

	   ` #listen_addresses='localhost'`

	   la riga:

	   `listen_addresses='*'`

	2. Aggiungere una riga al file pg_hba.conf:

	   `host    all             all             0.0.0.0/0               password`

5. Su CentOS invece sul file ph_hba.conf vanno sostituite tutte le voci *ident* con *md5*:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Local admninistrative login by Unix domain socket
local   all             postgres                                peer
# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     postgres                                peer
host    replication     postgres        127.0.0.1/32            md5
host    replication     postgres        ::1/128                 md5
# Let local users to connect from all networks using unencrypted password
host    all             all             0.0.0.0/0               password
```

## PostgreSQL come fonte dei dati su Grafana

- Aggiungere Data Source di tipo PostgreSQL, dove i parametri sono:
    - Host: *IP:porta*  nel caso di istanza Grafana su docker, l'IP è del tipo `172.17.0.1`. La porta standard è la 5432 per il PostgreSQL
    - Database: *grafana* o altro nome
    - Immettere _user_ e _password_ dell'utente che accede alla specifica istanza DB
    - TLS/SSL Mode: nel caso il DB sia locale, scegliere `disable` tra le opzioni

Sulla query, se si ha come formato della data una stringa del genere: `2021-09-06 11:55:37` allora bisogna usare la conversione a _UNIX TIMESTAMP_:

`> SELECT Extract(epoch From time::TIMESTAMP);`

Oppure:

`> SELECT to_timestamp(time,'YYYY-MM-DD HH24:MI:SS') as "time" ...`

Inoltre, assicurarsi che nella query **non** ci sia la stringa **`"time" as metrics`** altrimenti Grafana tratta ogni singolo valore di _timestamp_ come un singolo punto di coordinate (t,y).
Come esempio pratico, questa query estrae la colonna *bat_V* dalla tabella _data_ usando il timestamp in formato UNIX:
```
SELECT
  extract(epoch FROM time::TIMESTAMP) as "time",
  bat_V
FROM data
ORDER BY 1
```

## Configurazione di MariaDB/MySQL

La situazione di partenza è una installazione MariaDB con già configurata la password per l'amministratore (_root_) del server.

1. Entrare nel DBMS, creare il database (in questo caso chiamato **solarlogger**) e l'utente che ne avrà accesso (**grafana**, con password identica):
    ```
    $ sudo mysql -u root -p
    > SHOW DATABASES; # Mostra i DB presenti attualmente
    > CREATE DATABASE solarlogger;
    > CREATE USER 'grafana'@'localhost' IDENTIFIED BY 'grafana';
    > GRANT ALL PRIVILEGES ON solarlogger TO 'grafana'@'localhost';
    > FLUSH PRIVILEGES;
    > SHOW DATABASES;
    ```
2. Creare la tabella "data" dentro al DB _solarlogger_, dove si sono definite nel file **table.sql** la tipologia delle colonne:
    ```
    $ mysql -u grafana -D solarlogger -p < table.sql
    ```
3. Importare     
    > LOAD DATA LOCAL INFILE "/home/valerio/logs/base_all.csv" INTO TABLE solarlogger.data FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
    




## Temporaneo: in caso di problemi di permessi R/W tra utenti
Nel caso in cui da PSQL non si riesca a fare il COPY dei dati da CSV per problemi di accesso in lettura sulla cartella corrente, copiare i dati sulla **/tmp**, sulla quale hanno accesso tutti gli utenti indifferentemente


## Temporaneo: comandi per fare l'UPSERT sulla tabella *data*
- Insert new ingested data into temporary table *__data*

	`COPY __data FROM 'ingested.csv' DELIMITER ',' CSV HEADER;`
	
- Resolve conflicts on timestamp simply skipping data just into the DB

	`INSERT INTO data (SELECT * FROM __data) ON CONFLICT (Time) DO NOTHING;`
	
- Clear the temporary table

	`DELETE FROM __data;`

## Temporaneo: sostituire valori di misura mancante con 'NaN'

Individuate le colonne dove sono presenti valori non validi (es. 9999), per sostituirvi invece il valore 'NaN' si fa in un solo passaggio, colonna per colonna:

`UPDATE data SET bat_chg = 'NaN' WHERE bat_chg = 9999;`
