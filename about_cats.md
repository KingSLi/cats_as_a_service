## Analysis cats
### Feed the cat
UDP является ненадёжным: сообщения могут теряться в пути, дублироваться и переупорядочиваться. В данной задаче можем 
потерять последнее сообщение с ~ и операции зависнут, так же сообщения могут переупорядочиться и конечное сообщение придет 
в середине и тем самым у нас будут битые команды
Как улучшить? Можно добавить таймаут на получение всех частей сообщения, можно ввалидировать части, когда соединяешь их в одно целое
### Pet the cat
TCP неплох для данной задачи, кроме случаев, когда у нас слишком большой промежуток между запросами к серверу
(если наприер мы хотим гладить кота раз в 5 минут, то у нас постоянно будет висеть соединение).
Так же в данной задаче серверу необходимо парсить лог и проверять успешно ли покормил данный пользователь кота, а это довольно трудоемкая задача. 
Как улучшить? - Использовать для лога не html файл а базу данных или хранить в кэше последних успешных "кормильцев"

по UDP по сравнению с TCP, обмен данными происходит быстрее, но является ненадёжным: сообщения могут теряться в пути, дублироваться и переупорядочиваться.
