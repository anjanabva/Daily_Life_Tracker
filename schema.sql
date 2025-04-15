create database daily_life_tracker;
use daily_life_tracker;

create table users
(
user_id int primary key auto_increment,
user_name varchar(255) not null,
created_at timestamp default current_timestamp
);

create table diary_entries
(
entry_id int primary key auto_increment,
user_id int not null,
date date not null,
content text,
mood enum('fear', 'happy', 'sad', 'anger', 'contempt', 'nostalgia', 'other') not null,
tag enum('work', 'personal', 'travel', 'other') not null,
foreign key (user_id) references users(user_id) on delete cascade
);

create table expenses
(
expense_id int primary key auto_increment,
user_id int not null,
amount int not null,
category enum('food', 'shopping', 'grocery', 'health', 'other'),
date date not null,
description text,
foreign key (user_id) references users(user_id) on delete cascade
);

create table entertainment_tracker
(
entry_id int primary key auto_increment,
user_id int not null,
date date not null,
category enum('music', 'book', 'movie/series'),
title varchar(255) not null,
progress enum('not started', 'in progress', 'completed'),
foreign key (user_id) references users(user_id) on delete cascade
);

create table sleep_tracker
(
sleep_id int primary key auto_increment,
user_id int not null,
date date not null,
sleep_hours decimal(4,2) check (sleep_hours >= 0),
sleep_quality enum('poor', 'average', 'good', 'excellent'),
foreign key (user_id) references users(user_id) on delete cascade
);
