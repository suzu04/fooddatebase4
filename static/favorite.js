// ===========================
// ⭐ 設定
// ===========================
const STORAGE_KEY_FAV = "favorites";
const STORAGE_KEY_TAG = "tags";
const STORAGE_KEY_GROUP = "groups";


// ===========================
// ⭐ お気に入り GET / SAVE
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
// ⭐ 星の描画
// ===========================
function renderFavoriteStars() {
    const favIds = getFavorites().map(String);

    document.querySelectorAll(".fav").forEach(td => {
        const id = td.dataset.id;
        td.textContent = favIds.includes(id) ? "★" : "☆";
    });

    updateCompareCount();
}


// ===========================
// ⭐ 星トグル
// ===========================
function addFavoriteToggle() {
    document.querySelectorAll(".fav").forEach(td => {
        td.addEventListener("click", () => {
            const id = td.dataset.id;
            let favIds = getFavorites().map(String);

            if (favIds.includes(id)) {
                favIds = favIds.filter(x => x !== id);
                td.textContent = "☆";
            } else {
                favIds.push(id);
                td.textContent = "★";
            }

            saveFavorites(favIds);
            updateCompareCount();
        });
    });
}


// ===========================
// ⭐ 件数表示
// ===========================
function updateCompareCount() {
    const span = document.getElementById("compare-count");
    if (!span) return;
    span.textContent = getFavorites().length;
}


// ===========================
// ⭐ リセット
// ===========================
function setupResetButton() {
    const resetBtn = document.getElementById("resetStars");
    if (!resetBtn) return;

    resetBtn.addEventListener("click", () => {
        saveFavorites([]);
        document.querySelectorAll(".fav").forEach(td => td.textContent = "☆");
        updateCompareCount();
    });
}


// ===========================
// 📊 PFC比較へ
// ===========================
function setupPfcButton() {
    const btn = document.getElementById("pfcCompare");
    if (!btn) return;

    btn.addEventListener("click", () => {
        const ids = getFavorites();
        if (ids.length === 0) {
            alert("食品が選択されていません");
            return;
        }
        location.href = "/pfc-compare?ids=" + ids.join(",");
    });
}


// ===========================
// 🏷 タグ管理
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

    Object.entries(tags).forEach(([id, list]) => {
        const row = document.querySelector(`tr[data-id="${id}"]`);
        if (!row) return;

        const area = row.querySelector(".tag-area");
        if (area) {
            area.innerHTML = list.map(t => `<span class="tag">${t}</span>`).join("");
        }
    });
}

function openTagModal(id) {
    const tags = getTags();
    const current = tags[id] || [];

    const input = prompt(
        "タグをカンマ区切りで入力",
        current.join(",")
    );
    if (input === null) return;

    tags[id] = input.split(",").map(t => t.trim()).filter(Boolean);
    saveTags(tags);
    loadTags();
}

function addTagEditButtons() {
    document.querySelectorAll(".tag-edit").forEach(btn => {
        btn.addEventListener("click", () => {
            const row = btn.closest("tr");
            if (!row) return;
            openTagModal(row.dataset.id);
        });
    });
}


// ===========================
// 📦 グループ
// ===========================
function loadGroups() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY_GROUP) || "[]");
    } catch {
        return [];
    }
}

function saveGroups(groups) {
    localStorage.setItem(STORAGE_KEY_GROUP, JSON.stringify(groups));
}


// ===========================
// ⭐ 初期化
// ===========================
document.addEventListener("DOMContentLoaded", () => {
    renderFavoriteStars();
    addFavoriteToggle();
    setupResetButton();
    setupPfcButton();

    loadTags();
    addTagEditButtons();
});
