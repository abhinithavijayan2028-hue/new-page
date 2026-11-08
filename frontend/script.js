
function selectRole(role) {
    document.getElementById("selectedRole").innerText =
        "Selected module: " + role;
}

async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");
        const data = await response.json();

        document.getElementById("medicineCount").innerText =
            data.total_medicines;

        document.getElementById("stockCount").innerText =
            data.available_stock;

        document.getElementById("lowStock").innerText =
            data.low_stock;

        document.getElementById("salesCount").innerText =
            "₹" + data.today_sales;

    } catch (error) {
        console.error("Dashboard loading failed:", error);
    }
}

async function searchMedicine() {
    const name = document
        .getElementById("searchMedicine")
        .value.trim();

    const result = document.getElementById("searchResult");

    if (!name) {
        result.innerText = "Please enter a medicine name.";
        return;
    }

    try {
        const response = await fetch(
            "/api/medicines?search=" + encodeURIComponent(name)
        );

        const data = await response.json();

        if (data.length === 0) {
            result.innerText = "No medicine found.";
        } else {
            result.innerText = data.map(
                medicine => medicine.name +
                " - Stock: " + medicine.quantity
            ).join(" | ");
        }

    } catch (error) {
        result.innerText = "Unable to search medicines.";
    }
}

loadDashboard();
