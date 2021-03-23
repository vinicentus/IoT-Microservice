FROM ubuntu:latest

# INSTALL CRON
RUN apt-get update
RUN apt-get install cron

# ADD CRONTAB FILE TO THE CRON DIR
ADD crontab /etc/cron.d/microservice-cron

# ADD SPS30_DRIVER
#COPY URL DEST
#RUN curl

# ADD SPS30 SCRIPTS AND GRANT EXECUTION RIGHTS
COPY sps30_sensor_clean.py /sps30_sensor_clean.py
RUN chmod +x /sps30_sensor_clean.py

COPY sps30_collect_data.py /sps30_collect_data.py
RUN chmod +x /sps30_collect_data.py

# GIVE EXECUTION RIGHTS TO THE CRON JOB
RUN chmod 0644 /etc/cron.d/microservice-cron

# CREATE CRON LOG FILE
RUN touch /var/log/cron.log

# RUN CRON ON CONTAINER STARTUP
CMD cron && tail -f /var/log/cron.log
