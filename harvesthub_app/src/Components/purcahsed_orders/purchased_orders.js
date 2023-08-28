import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './PurchaseHistory.css'; // Add your CSS styles here
import { ALL_ORDERS } from '../../constants';

const PurchaseHistory = () => {
    const [rowData, setRowData] = useState([]);

    useEffect(() => {
        const options = {
            withCredentials: true,
            credentials: 'same-origin',

            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                'Content-Type': 'application/json',
            },
        };
        
        axios.get(ALL_ORDERS, options)
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
        { headerName: 'View', field: 'view'},
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