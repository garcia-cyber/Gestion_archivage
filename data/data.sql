-- creation data


create schema if not exists sonas;
use sonas;

-- table des acces et insertion des acces utilise


create table acces(
    id_acces tinyint auto_increment primary key,
    type_ varchar(15)
);

insert into acces(type_)values('admin'),('secretaire'),('archiviste');

-- table login

create table logins(
    id_login tinyint auto_increment primary key,
    username varchar(20),
    pwd varchar(255),
    email varchar(100)
);

alter table logins add type_acces tinyint;
alter table logins add constraint fk_login foreign key(type_acces) references acces(id_acces) on delete set null 
on update cascade;

-- table secret mot de passe  et mot de passe aleatoire
create table secret(
    id_secre tinyint auto_increment primary key,
    pwd varchar(100)
);

insert into secret_(secret_pwd)values('sonas');

-- table departement et commune plus insertion 

create table departements(
    id_depart tinyint auto_increment primary key,
    type_depart varchar(20)
);

insert into departements(type_depart)values('commercial'),('informatique');

create table communes(
    id_commune tinyint auto_increment primary key,
    libelle varchar(20)
);

insert into communes(libelle)values('Limete'),('Matete'); 

-- create table agent 

create table agents(
    id_agent smallint auto_increment primary key,
    nom varchar(50),
    postnom varchar(50),
    prenom varchar(40),
    sexe char(1),
    adresse varchar(100),
    commune tinyint ,
    phone varchar(15),
    date_embauche date default curdate(),
    departement tinyint

);

-- NB commune et departement sont de  cle etrangere

-- ajout des cles etrangeres 

alter table agents add constraint fk_depart foreign key(departement) references departements(id_depart) on delete set null 
on update cascade , add constraint fk_commune foreign key(commune) references communes(id_commune) on delete set null 
on update cascade ;
