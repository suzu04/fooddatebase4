<?php
// 検索したい食品名（ここを書き換えればOK）
$searchName = "アマランサス 玄穀";

// ファイル名とカテゴリの対応
$files = [
    "data012.csv" => "栄養素",
    "data022.csv" => "アミノ酸",
    "data032.csv" => "脂肪酸",
    "data042.csv" => "炭水化物"
];

// ディレクトリ名（ファイルの場所）
$dir = __DIR__ . "/csvviewer";

foreach ($files as $filename => $label) {
    $path = "$dir/$filename";
    echo "=== {$label} ({$filename}) ===\n";

    if (!file_exists($path)) {
        echo "ファイルが見つかりません: $filename\n";
        continue;
    }

    $handle = fopen($path, "r");
    if (!$handle) {
        echo "ファイルを開けませんでした: $filename\n";
        continue;
    }

    $header = fgetcsv($handle);
    $found = false;

    while (($row = fgetcsv($handle)) !== false) {
        $rowAssoc = array_combine($header, $row);
        if (strpos($rowAssoc["name"], $searchName) !== false) {
            foreach ($rowAssoc as $key => $value) {
                echo "{$key}: {$value}\n";
            }
            $found = true;
            break;
        }
    }

    fclose($handle);

    if (!$found) {
        echo "{$searchName} は見つかりませんでした。\n";
    }

    echo "\n";
}
?>
