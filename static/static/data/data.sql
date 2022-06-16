create table user_chef(
    id_login tinyint auto_increment primary key,
    username varchar()
)


+------------+---------------------+------+-----+---------+----------------+
| Field      | Type                | Null | Key | Default | Extra          |
+------------+---------------------+------+-----+---------+----------------+
| id_chef    | tinyint(4)          | NO   | PRI | NULL    | auto_increment |
| nom        | varchar(50)         | YES  |     | NULL    |                |
| postnom    | varchar(50)         | YES  |     | NULL    |                |
| prenom     | varchar(50)         | YES  |     | NULL    |                |
| adresse    | varchar(100)        | YES  |     | NULL    |                |
| telephone  | varchar(15)         | YES  |     | NULL    |                |
| commune    | varchar(20)         | YES  |     | NULL    |                |
| sexe       | varchar(15)         | YES  |     | NULL    |                |
| civilite   | varchar(15)         | YES  |     | NULL    |                |
| date_nai   | date                | YES  |     | NULL    |                |
| lieu_nai   | varchar(50)         | YES  |     | NULL    |                |
| secteur    | varchar(50)         | YES  |     | NULL    |                |
| territoire | varchar(50)         | YES  |     | NULL    |                |
| province   | tinyint(3) unsigned | YES  | MUL | NULL    |                |
| cellule    | varchar(20)         | YES  |     | NULL    |                |
| pwd        | varchar(255)        | YES  |     | NULL    |                |
+------------+---------------------+------+-----+---------+----------------+


