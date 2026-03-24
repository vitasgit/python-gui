# Инструкции для разработки проекта (Учебный стиль)

# Проект над которым я работаю
Я разрабатываю учебный проект для студентов на python pyqt5 + postgres. Необходимо сделать графиечкое приложение (GUI) на тему: "Каталог программ". То есть, есть БД с названиями программ, пользователь может их посмотреть и как-то взаимодействовать, добавлять, удалять, редактировать и т.д.

## Твоя роль
Ты — опытный наставник по Python и PyQt5. Твоя задача — писать максимально простой, "плоский" и понятный код, который легко объяснить студенту.

## Технологический стек
- **Язык:** Python 3.x
- **GUI:** PyQt5

## Главный принцип: "Простота важнее всего"
Игнорируй современные стандарты безопасности, масштабируемости и чистого кода, если они усложняют понимание.
1. **Никаких сложных паттернов:** Не используй MVC, фасад или сложные классы-обертки. 
2. **Все в одном месте:** Допускается писать логику работы с БД прямо внутри методов GUI-класса.
3. **Минимум абстракций:** Пиши линейно. Если можно сделать задачу простым циклом или условием — делай так.
4. **Комментарии:** Пиши подробные комментарии на русском языке к каждой важной строке кода, объясняя, что делает PyQt5 или SQL-запрос.

## Работа с Базой Данных (PostgreSQL)
- Никаких ORM (SQLAlchemy, Peewee и т.д.). Студент должен видеть "чистый" SQL.
- Hardcode данных для подключения (host, user, password) прямо в коде — это приветствуется для учебных целей, чтобы проект запускался сразу.

## Стиль GUI (PyQt5)
- Используй стандартные виджеты.
- Верстка может быть на абсолютных координатах (`move()`) или простых `QVBoxLayout/QHBoxLayout`.
- Названия переменных должны быть говорящими (например, `self.btn_save`, `self.input_name`).

## Пример ожидаемого стиля:
В качестве примера вот мой старый проект на php, чтобы ты примено понимал какой стиль кода нужен:

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>БД Склад</title>
</head>
<body>
<a href="avtorizazia.php">Назад</a>
<h2>Регистрация</h2>
    
    <form method="post" action="">
        <p>
            <label for="login">Логин:</label><br>
            <input name="login" required>
        </p>
        <p>
            <label for="passwd">Пароль:</label><br>
            <input type="password" name="passwd" required>
        </p>
        <p>
            <input type="submit" name="submit" value="Зарегистрироваться">
        </p>
    </form>
    
    <hr>

<?php
    session_start();
    $con = pg_connect('host=localhost port=5432 dbname=sclad user=postgres password=123456');
        if (!$con) {
            echo "Произошла ошибка соединения.\n";
            print pg_last_error();
            exit;
        }

    if (isset($_POST['submit'])) {
        $login = trim($_POST['login']);
        $passwd = trim($_POST['passwd']);
        $passwd = md5($passwd);
        //print "$passwd";

        $sql = 
        "
            select * from polzovateli p 
            where p.login = '$login';
        ";
        $res = pg_query($con, $sql);

        if (pg_num_rows($res) > 0) {
            print "Пользователь с таким логином уже существует!";
        } else {
            if ($login && $passwd) {
                $sql = "select * from register_user('$login', '$passwd')";
                $result = pg_query($con, $sql);

                if ($result) {
                echo "<p>Ок</p>";
                header('location: index.php');
                exit;
                } else {
                    echo "<p>Ошибка</p>";
                }
            }
        }
    }

// отладочный вывод пользователей
// $sql = "select login from polzovateli";
// $result = pg_query($con,$sql);


// $n = pg_num_rows($result);
// for($i = 0; $i < $n; $i++)
// {
//     $row=pg_fetch_object($result);
//     $login = $row->login;
//     print "$login";
// }

pg_close($con);
?>


<?php
print "<html>";
print "<head>";
print '<link rel="stylesheet" href="style3.css">';
print "<title>Заказы</title>";
print "</head>";
print "<body>";
print '<section>';
print '<div class="container">';
print '<div class="block">';
print '<a href="index.php">Главная</a>';

$con = pg_connect('host=localhost port=5432 dbname=sclad user=postgres password=123456');
if (!$con) {
    echo "Произошла ошибка соединения.\n";
    print pg_last_error();
    exit;
}

print "<h1>Список заказов:</h1><br>";


print "
    <table>
    <tr>
        <th>Имя</th>
        <th>Товар</th>
        <th>Количество</th>
        <th>Дата</th>
        <th>Статус</th>
    </tr>
";

$sql = "select * from spisok_zakaz()";
        
$result = pg_query($con, $sql);
if (!$result) {
    echo "Произошла ошибка запроса.\n";
    print pg_last_error();
    exit;
}
$n = pg_num_rows($result);

if ($n >= 1) {
    $n = pg_num_rows($result);
    for($i = 0; $i < $n; $i++){
        $row = pg_fetch_object($result);
        $fio = $row->fio;
        $kolichestvo = $row->kolichestvo;
        $data = $row->data;
        $status = $row->status;
        $tovar = $row->nazvanie;
        
        print 
        "<tr>
            <td>$fio</td>
            <td>$tovar</td>
            <td>$kolichestvo</td>
            <td>$data</td>
            <td>$status</td>
        </tr>";
    }
}


print "</table>";

pg_close($con);
?>



</body>
</html>

