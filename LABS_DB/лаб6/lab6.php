<?php
$link = mysqli_connect("localhost", "root", "1380", "Тагиров");
if (!$link) { die("Ошибка подключения: " . mysqli_connect_error()); }

if (isset($_POST['view'])) {
    $view = $_POST['view'];
    $msg = "";

    if ($view == '1') {
        $sql = "SELECT * FROM View_Employees_Contact";
        $title = "Представление 1: Сотрудники (Телефон, ЗП)";
    } elseif ($view == '2') {
        $sql = "SELECT * FROM View_Employees_Address";
        $title = "Представление 2: Сотрудники с адресами";
    } elseif ($view == '3') {
        $sql = "SELECT * FROM View_Employees_Experience";
        $title = "Представление 3: Сотрудники со стажем > 4";
    }

    $res = mysqli_query($link, $sql);
    $msg = "<h3>$title</h3>";
    $msg .= "<table border='1' cellpadding='5'><tr>";
    
    // Выводим заголовки колонок
    $fields = mysqli_fetch_fields($res);
    foreach ($fields as $field) {
        $msg .= "<th>{$field->name}</th>";
    }
    $msg .= "</tr>";

    // Выводим данные
    while ($row = mysqli_fetch_assoc($res)) {
        $msg .= "<tr>";
        foreach ($row as $value) {
            $msg .= "<td>$value</td>";
        }
        $msg .= "</tr>";
    }
    $msg .= "</table>";

    mysqli_close($link);
    echo $msg;
    exit;
}
?>

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №6: VIEW</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f4f4f9; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; margin-bottom: 20px; }
        .buttons { display: flex; gap: 10px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap; }
        button { padding: 10px 20px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2980b9; }
        .result { border: 1px solid #ddd; padding: 20px; border-radius: 5px; min-height: 200px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; margin-top: 10px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #eee; }
    </style>
    <script>
        function runView(n) {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "Загрузка...";
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "lab6.php", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onload = function() { resultDiv.innerHTML = xhr.responseText; };
            xhr.send("view=" + n);
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Лабораторная работа №6: Представления (VIEW)</h1>
        <div class="buttons">
            <button onclick="runView(1)">Представление 1</button>
            <button onclick="runView(2)">Представление 2</button>
            <button onclick="runView(3)">Представление 3</button>
        </div>
        <div class="result" id="result">
            Нажмите на кнопку, чтобы вывести данные из представления.
        </div>
    </div>
</body>
</html>
