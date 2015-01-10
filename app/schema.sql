drop table if exists alerts;
create table alerts (
    alert_id integer primary key autoincrement,
    rname text not null,
    rid integer not null,
    start_date text not null,
    end_date text not null,
    start_time text not null,
    end_time text not null,
    people text not null,
    email text not null,
    status text not null
    );