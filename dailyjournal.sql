insert into 'Entries' value (null, 'Javascript','I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', '1', 'Wed Sep 15 2021 10:10:47 ')
insert into 'Entries' value (null, 'Python',"Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", '4', 'Wed Sep 15 2021 10:10:47 ')
insert into 'Entries' value (null, 'Python',"Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks", '4', 'Wed Sep 15 2021 10:10:47 ')
insert into 'Entries' value (null, 'Javascript',"Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", '4', 'Wed Sep 15 2021 10:10:47 ')

select 
    e.id,
    e.concept,
    e.entry,
    e.date,
    e.mood_id,
    m.label entry_mood
from Entries e 
join Moods m 
    on m.id = e.mood_id
    