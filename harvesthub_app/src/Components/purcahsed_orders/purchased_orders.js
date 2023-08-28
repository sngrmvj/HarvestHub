import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './PurchaseHistory.css'; // Add your CSS styles here

const PurchaseHistory = () => {
    const [rowData, setRowData] = useState([]);

    useEffect(() => {
        // Fetch purchase history from the backend using Axios
        axios.get('your_backend_endpoint')
            .then(response => {
                setRowData(response.data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const columnDefs = [
        { headerName: 'Date', field: 'date', sortable: true, filter: true },
        { headerName: 'Item', field: 'item', sortable: true, filter: true },
        { headerName: 'Quantity', field: 'quantity', sortable: true, filter: true },
        { headerName: 'Price', field: 'price', sortable: true, filter: true },
    ];

    return (
        <div className="purchase-history-container">
            <h1>Purchase History</h1>
            <div className="ag-theme-alpine ag-grid-container">
                <AgGridReact
                    rowData={rowData}
                    columnDefs={columnDefs}
                    pagination={true}
                />
            </div>
        </div>
    );
}

export default PurchaseHistory;