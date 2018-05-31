
/*create data base*/
create schema if not exists bugzilla default character set utf8 collate utf8_general_ci;

/*create user */
create user if not exists 'dataApp'@'%' identified by 'newsys';

/*grant to user*/
grant all privileges on bugzilla.* to dataApp;


/*works now*/
flush privileges;
