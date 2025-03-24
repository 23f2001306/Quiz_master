document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector("[data-search]");
    const tableBody = document.querySelector("[data-table-body]");
    const apiUrl = searchInput.getAttribute("data-api"); 
    const field = searchInput.getAttribute("data-field"); 

    let items = [];

    fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
            items = data;
            displayItems(items); 
        })
        .catch(error => console.error("Error fetching data:", error));


    searchInput.addEventListener("input", function (e) {
        const value = e.target.value.toLowerCase();
        const filteredItems = items.filter(item => 
            item[field].toLowerCase().includes(value)
        );
        displayItems(filteredItems);
    });

    function displayItems(items) {
        tableBody.innerHTML = ""; 
        if (items.length > 0) {
            items.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.quiz_name}</td>
                    <td>${item.total_scored} / 100</td>
                    <td>${item.timestamp}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center">No quiz attempts found.</td>
                </tr>
            `;
        }
    }
});