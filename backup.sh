export PGUSER=webuser_fiesta
export PGPASSWORD=gdu71B2-miu95K

/opt/PostgreSQL/9.2/bin/pg_dump fiesta | gzip > /home/webuser007/bak/fiesta_$(date +%Y-%m-%d).gz

cp /var/redis/dump.rdb /home/webuser007/bak/redis_dump_$(date +%Y-%m-%d).rdb