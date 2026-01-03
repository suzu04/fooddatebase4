<?php
// ここではGETで受け取った内容を表示するだけ（デモ用）

$query = $_GET['query'] ?? '';
$category = $_GET['category'] ?? '';
$date_from = $_GET['date_from'] ?? '';
$date_to = $_GET['date_to'] ?? '';
$sort = $_GET['sort'] ?? '';
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>検索結果</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <h1>検索結果</h1>

    <div class="search-result">
        <p><strong>キーワード:</strong> <?= htmlspecialchars($query) ?></p>
        <p><strong>カテゴリ:</strong> <?= htmlspecialchars($category) ?></p>
        <p><strong>日付:</strong> <?= htmlspecialchars($date_from) ?> ～ <?= htmlspecialchars($date_to) ?></p>
        <p><strong>並び順:</strong> <?= htmlspecialchars($sort) ?></p>
    </div>

</body>
</html>
