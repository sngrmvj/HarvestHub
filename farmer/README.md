### Farmer




```
<link rel="stylesheet" href="{{ url_for('static', filename='path-to-ag-grid-styles.css') }}">
<script src="{{ url_for('static', filename='path-to-ag-grid.js') }}"></script>
<div id="myGrid" style="height: 400px;" class="ag-theme-alpine"></div>
<script>
    document.addEventListener('DOMContentLoaded', function () {
        var gridOptions = {
            columnDefs: [
                { headerName: "Make", field: "make" },
                { headerName: "Model", field: "model" },
                { headerName: "Price", field: "price" }
            ],
            rowData: [
                { make: "Toyota", model: "Celica", price: 35000 },
                { make: "Ford", model: "Mondeo", price: 32000 },
                { make: "Porsche", model: "Boxster", price: 72000 }
            ],
            defaultColDef: {
                sortable: true,
                resizable: true
            }
        };

        var gridDiv = document.querySelector('#myGrid');
        new agGrid.Grid(gridDiv, gridOptions);
    });
</script>


"""" Prefer below one

<div id="myGrid" style="height: 400px;" class="ag-theme-alpine"></div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        var gridOptions = {
            columnDefs: [
                { headerName: "Make", field: "make" },
                { headerName: "Model", field: "model" },
                { headerName: "Price", field: "price" }
            ],
            rowData: {{ row_data | tojson | safe }},
            defaultColDef: {
                sortable: true,
                resizable: true
            }
        };

        var gridDiv = document.querySelector('#myGrid');
        new agGrid.Grid(gridDiv, gridOptions);
    });
</script>

https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template

"""" -> Belowone is previous


<div id="myGrid" class="ag-theme-alpine" style="height: 500px"></div>
<script type="text/javascript">
    const gridOptions = {
        columnDefs: [
            { field: "Farmer Name" },
            { field: "Agent ID" },
            { field: "Date" },
            { field: "View" },
        ],

        // default col def properties get applied to all columns
        defaultColDef: {sortable: true, filter: true},

        rowSelection: 'multiple', // allow rows to be selected
        animateRows: true, // have rows animate to new positions when sorted
            // example event handler
        onCellClicked: params => {
            console.log('cell was clicked', params)
        }
    };
    const eGridDiv = document.getElementById("myGrid");
    new agGrid.Grid(eGridDiv, gridOptions);

    // Fetch data from server
    fetch("{{ url_for('get_receipts') }}")
    .then(response => response.json())
    .then(data => {
        // load fetched data into grid
        gridOptions.api.setRowData(data);
    });
</script>

```