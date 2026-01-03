// ===========================
// ⭐ 設定
// ===========================
const STORAGE_KEY_FAV = "favorites";
const STORAGE_KEY_TAG = "tags";


// ===========================
// ⭐ お気に入りデータ GET / SAVE
// ===========================
function getFavorites() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY_FAV) || "[]");
    } catch {
        return [];
    }
}

function saveFavorites(list) {
    localStorage.setItem(STORAGE_KEY_FAV, JSON.stringify(list));
}


// ===========================
// ⭐ お気に入りのDOM反映
// ===========================
function renderFavoriteStars() {
    const favIds = getFavorites();

    document.querySelectorAll(".fav").forEach(td => {
        const id = td.dataset.id;
        td.textContent = favIds.includes(id) ? "★" : "☆";
    });

    updateCompareCount();
}


// ===========================
// ⭐ 初期化
// ===========================
document.addEventListener("DOMContentLoaded", () => {
    renderFavoriteStars();
    addFavoriteToggle();

    loadTags();
    addTagEditButtons();
});


// ===========================
// ⭐ トグル機能
// ===========================
function addFavoriteToggle() {
    const favCells = document.querySelectorAll(".fav");

    favCells.forEach(td => {
        td.onclick = () => {
            const id = td.dataset.id;
            let favIds = getFavorites();

            if (favIds.includes(id)) {
                favIds = favIds.filter(x => x !== id);
                td.textContent = "☆";
            } else {
                favIds.push(id);
                td.textContent = "★";
            }

            saveFavorites(favIds);
            updateCompareCount();
        };
    });
}


// ===========================
// ⭐ 選択数の表示更新
// ===========================
function updateCompareCount() {
    const favIds = getFavorites();
    const span = document.getElementById("compare-count");
    if (span) span.textContent = favIds.length;
}


// ===========================
// ⭐ タグ管理（保存/読み込み）
// ===========================
function getTags() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY_TAG) || "{}");
    } catch {
        return {};
    }
}

function saveTags(tags) {
    localStorage.setItem(STORAGE_KEY_TAG, JSON.stringify(tags));
}

function loadTags() {
    const tags = getTags();

    Object.keys(tags).forEach(id => {
        const row = document.querySelector(`tr[data-id="${id}"]`);
        if (!row) return;

        const tagArea = row.querySelector(".tag-area");
        if (tagArea) {
            tagArea.innerHTML = tags[id].map(t => `<span class="tag">${t}</span>`).join("");
        }
    });
}

function addTagEditButtons() {
    document.querySelectorAll("tr[data-id]").forEach(row => {
        const id = row.dataset.id;
        const btn = row.querySelector(".tag-edit");

        if (!btn) return;

        btn.onclick = () => openTagModal(id);
    });
}


// ===========================
// ⭐ タグ編集モーダル
// ===========================
function openTagModal(id) {
    const tags = getTags();
    const currentTags = tags[id] || [];

    const tagText = prompt(
        "この食材のタグをカンマ区切りで入力:\n例: 高タンパク, 低脂質",
        currentTags.join(",")
    );

    if (tagText === null) return;

    const newTags = tagText
        .split(",")
        .map(t => t.trim())
        .filter(t => t);

    tags[id] = newTags;
    saveTags(tags);

    loadTags();
}

// ===========================
// ⭐ リセットボタン
// ===========================
document.addEventListener("DOMContentLoaded", () => {
    const resetBtn = document.getElementById("resetStars");
    if (resetBtn) {
        resetBtn.onclick = () => {
            // お気に入りをすべて削除
            saveFavorites([]);

            // 全ての星を「☆」に戻す
            document.querySelectorAll(".fav").forEach(td => {
                td.textContent = "☆";
            });

            // 件数を 0 に更新
            updateCompareCount();
        };
    }
});


// ===========================
// 📊 PFC比較へ
// ===========================
document.addEventListener("DOMContentLoaded", () => {
    const pfcBtn = document.getElementById("pfcCompare");
    if (pfcBtn) {
        pfcBtn.onclick = () => {
            const favIds = getFavorites();

            // IDの配列 → 1,23,55 のように結合
            const url = "/pfc-compare?ids=" + favIds.join(",");

            // ページ移動
            window.location.href = url;
        };
    }
});

// グループ操作用の共通関数
function loadGroups() {
    return JSON.parse(localStorage.getItem("groups") || "{}");
}

function saveGroups(groups) {
    localStorage.setItem("groups", JSON.stringify(groups));
}


