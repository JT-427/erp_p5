const tableSearchInput = document.getElementById('tableSearchInput');
tableSearchInput.addEventListener('keyup', (event) => {
    const table = document.getElementById('dataTable');
    // Declare variables 
    filter = event.target.value.trim();
    tr = table.querySelector('tbody').getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i=0; i<tr.length; i++) {
        let tds = tr[i].querySelectorAll("td, th");
        for(g=0; g<tds.length; g++){
            let td = tds[g];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break;
                } else {
                    tr[i].style.display = "none";
                    continue;
                }
            }
        }
    }
})