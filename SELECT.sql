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

--4e ДЗ
--количество исполнителей в каждом жанре;

select s.name, COUNT(m.name) from styles s 
join musicians_styles ms on s.id  = ms.style_id  
join musicians m on ms.style_id = m.id
group by s.name

--количество треков, вошедших в альбомы 2019-2020 годов;
select count(s.name) from albums a
join songs s on a.id = s.album_id 
where a.year >= 2019 and a.year <= 2020

--средняя продолжительность треков по каждому альбому;

select a.name, avg(s.duration)  from albums a 
join songs s on a.id = s.album_id 
group by a.name


--все исполнители, которые не выпустили альбомы в 2020 году;
select m.name from musicians m 
join musicians_albums ma on ma.musician_id = m.id 
join albums a on a.id = ma.album_id 
where a.year = 2020

--названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
select c.name from collections c 
join songs_collections sc on c.id = sc.collection_id 
join songs s on s.id = sc.song_id 
join musicians_albums ma on s.album_id = ma.album_id 
join musicians m on m.id = ma.musician_id 
where m.name like '%Кино%'


--название альбомов, в которых присутствуют исполнители более 1 жанра;
-- не смог понять как сделать, потогайте
select * from albums a 
join musicians_albums ma on ma.album_id = a.id 
join musicians_styles ms on ms.musician_id = ma.musician_id 
join styles s on s.id = ms.style_id 
order by (s.id > 1)


-- наименование треков, которые не входят в сборники;
select s.name  from songs s 
left join songs_collections sc on s.id = sc.song_id 
where sc.collection_id is null

-- исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
select m.name from musicians m 
join musicians_albums ma on ma.musician_id = m.id 
join songs s on s.album_id = ma.album_id 
where s.duration = (select min(s2.duration) from songs s2)

--название альбомов, содержащих наименьшее количество треков.
-- похожая проблема, не пойму как считать количество
select * from albums a 
join songs s on s.album_id = a.id
