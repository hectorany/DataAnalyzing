FROM mysql

# Environment variables
ENV MYSQL_ROOT_PASSWORD root
#
# # Allows you to change the value of "max_allowed_packet"
# ADD ["mysqlconf/gatewaymy.cnf", "/etc/mysql/conf.d/conf_mysql.cnf"]
#
# # Create Database
#
COPY sql/sources.sql  /docker-entrypoint-initdb.d
#
#PORT
EXPOSE 3306
