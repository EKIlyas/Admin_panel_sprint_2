create schema if not exists content;
set search_path to content;

create type role as enum ('director', 'writer', 'actor');

create table if not exists person(
    id uuid primary key,
    full_name varchar(255) not null,
    birth_date date,
    created_at timestamptz,
    updated_at timestamptz
);

create table if not exists genre(
    id uuid primary key,
    name varchar(255) not null,
    description text,
    created_at timestamptz,
    updated_at timestamptz
);

create table if not exists film_work(
    id uuid primary key,
    title varchar(255) not null,
    description text,
    creation_date date,
    certificate varchar(255),
    file_path varchar(255),
    rating float4,
    type varchar(255),
    created_at timestamptz,
    updated_at timestamptz
);

create table if not exists person_film_work(
    id uuid primary key,
    film_work_id uuid not null,
    person_id uuid not null,
    role role,
    created_at timestamptz
);

create table if not exists genre_film_work(
    id uuid primary key,
    genre_id uuid not null,
    film_work_id uuid not null,
    created_at timestamptz
);

create unique index person_role_film on person_film_work(person_id, film_work_id, role);
create unique index genre_film on genre_film_work(film_work_id, genre_id);
