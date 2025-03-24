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
      if (items.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="2" class="text-center">No data found.</td>
            </tr>
        `;
    } else {
        
        items.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item[field]}</td>
                <td>
                    <button class="btn btn-primary btn-sm" onclick="viewItem(${item.id})">View</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }
  }

  window.viewItem = function (itemId) {
      const viewUrl = searchInput.getAttribute("data-view-url"); 
      window.open(viewUrl + itemId, 'View Details', 'width=800,height=350');
  };
});
