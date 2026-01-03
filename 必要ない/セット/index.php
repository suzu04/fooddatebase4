<?php
$keyword = isset($_GET['keyword']) ? $_GET['keyword'] : '';
$csv_dir = __DIR__ . '/CSVfile/';
$files = scandir($csv_dir);

$results = [];

foreach ($files as $file) {
    if (pathinfo($file, PATHINFO_EXTENSION) !== 'csv') continue;

    $rows = array_map('str_getcsv', file($csv_dir . $file));
    foreach ($rows as $row) {
        foreach ($row as $col) {
            if (stripos($col, $keyword) !== false) {
                $results[] = $row;
                break;
            }
        }
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>CSV検索</title>
</head>
<body>
    <form method="get">
        <input type="text" name="keyword" placeholder="検索キーワード" value="<?= htmlspecialchars($keyword) ?>">
        <button type="submit">検索</button>
    </form>

    <h2>検索結果:</h2>
    <table border="1">
        <?php foreach ($results as $row): ?>
            <tr>
                <?php foreach ($row as $col): ?>
                    <td><?= htmlspecialchars($col) ?></td>
                <?php endforeach; ?>
            </tr>
        <?php endforeach; ?>
    </table>
</body>
</html>
