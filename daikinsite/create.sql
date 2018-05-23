create table if not exists "seinfo"(
  id varchar(20),
  fullname varchar(30),
  email varchar(50),
  skilllevel varchar(20),
  purchasedate date,
  latitude decimal,
  longitude decimal,
  rating decimal,
  primary key(id)
);

create table if not exists "dealerinfo"(
  id varchar(20),
  fullname varchar(30),
  email varchar(50),
  SE varchar(50),
  purchasedate date,
  latitude decimal,
  longitude decimal,
  address varchar(20),
  primary key(id),
  foreign key (SE) references seinfo on delete cascade
);

create table if not exists "customerinfo"(
  id varchar(20),
  fullname varchar(30),
  email varchar(50),
  system varchar(50),
  purchasedate date,
  dealerid varchar(20),
  latitude decimal,
  longitude decimal,
  address varchar(20),
  primary key(id, system),
  foreign key (dealerid) references dealerinfo on delete cascade
);

create table if not exists "expertinfo"(
  id varchar(20),
  fullname varchar(30),
  email varchar(50),
  primary key(id)
);

create table if not exists "analystinfo"(
  id varchar(20),
  fullname varchar(30),
  email varchar(50),
  primary key(id)
  );

create table if not exists "notifications"(
  senderid varchar(20),
  receiverid varchar(20),
  description varchar(100),
  primary key(senderid, receiverid, description)
  );

create table if not exists "components"(
  ownerid varchar(20),
  compname varchar(40),
  count integer,
  description varchar(100),
  primary key (ownerid, compname)
  );
