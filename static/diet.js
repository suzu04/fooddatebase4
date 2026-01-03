document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action='/search']");
    const dietCheckbox = document.getElementById("diet-checkbox");

    if (!form || !dietCheckbox) return;

    form.addEventListener("submit", (e) => {
        // チェックされていたらリダイレクト
        if (dietCheckbox.checked) {
            e.preventDefault();  // デフォルトの検索処理を止める
            window.location.href = "/diet?type=diet";
        }
    });
});

// --- たんぱく質列で初期ソート ---    
document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("foodTable");
    if (!table) return;

    const protIndex = 4; // たんぱく質列
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    // 数値として降順ソート（高タンパク順）
    rows.sort((a, b) => {
        const aVal = parseFloat(a.children[protIndex].innerText) || 0;
        const bVal = parseFloat(b.children[protIndex].innerText) || 0;
        return bVal - aVal;
    });

    tbody.innerHTML = "";
    rows.forEach(r => tbody.appendChild(r));
});
