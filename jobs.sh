#!/bin/bash
export PATH=$PATH:/opt/PostgreSQL/9.2/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/PostgreSQL/9.2/lib
cd /home/webuser007/.virtualenvs/fiesta/bin/
source /home/webuser007/.virtualenvs/fiesta/bin/activate
python /home/webuser007/web/fiesta/manage.py mark_news_as_archive
