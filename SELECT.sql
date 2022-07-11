SELECT name,year FROM albums
where year = 2018

SELECT name, duration FROM songs 
order by duration desc 
limit 1

SELECT name FROM songs
where duration > 210

SELECT name FROM collections
where year >= 2018 and year <= 2020

SELECT name FROM musicians
where name not LIKE '% %'

SELECT name FROM songs
where name LIKE '%Мой%' or name LIKE '%my%'