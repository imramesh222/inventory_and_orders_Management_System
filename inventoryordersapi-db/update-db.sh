#!/bin/bash
cd "$(dirname "$0")"
liquibase \
  --changeLogFile=db/changelog-master.xml \
  --url=jdbc:postgresql://localhost:5432/inventory_db \
  --username=postgres \
  --password=ramesh \
  --classpath=./postgresql-42.6.0.jar \
  update