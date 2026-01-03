document.getElementById("search-form").addEventListener("submit", function (e) {
    e.preventDefault();
    const keyword = document.getElementById("keyword").value.trim();
    const tbody = document.querySelector("#results tbody");
    const noResult = document.getElementById("no-result");
    tbody.innerHTML = "";

    fetch("data/items.csv")
        .then(res => res.text())
        .then(text => {
            const rows = text.split("\n").slice(1); // 1行目はヘッダー
            const matched = rows.filter(row => row.toLowerCase().includes(keyword.toLowerCase()));

            if (matched.length === 0) {
                noResult.style.display = "block";
            } else {
                noResult.style.display = "none";
                matched.forEach(row => {
                    const cols = row.split(",");
                    const tr = document.createElement("tr");
                    cols.forEach(col => {
                        const td = document.createElement("td");
                        td.textContent = col;
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                });
            }
        })
        .catch(err => console.error("CSV読み込みエラー:", err));
});

