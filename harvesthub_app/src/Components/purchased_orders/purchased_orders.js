import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import './purchased_orders.css'; // Add your CSS styles here
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ALL_ORDERS, VALIDATE_USER } from '../../constants';

const PurchaseHistory = () => {
    const [rowData, setRowData] = useState([
        {'Date': "Null", 'Item': 'Tomato', 'Quantity': '20', 'Price': '40'} 
    ]);
    const [name, setName] = useState(localStorage.getItem('fullname'));
    const navigate = useNavigate();

    const navigateToMenu = () => {
        navigate('/menu');
    }

    const navigateToReceipt = (data) => {
        navigate("/receipt",{ state: { data: data } })
    }

    const logout = () =>{
        localStorage.setItem('isLoggedIn',false);
        localStorage.removeItem('email');
        localStorage.removeItem('fullname');
        navigate("/")
    }

    const validAuthentication = () => {
        axios.get(`${VALIDATE_USER}`)
        .then((res) => {
            console.log("Carry On!!");
        })
        .catch((error) => {
            toast.error("User Autentication Failed");
            logout();
        })
    }

    useEffect(() => {

        validAuthentication();

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
                console.log(response);
                setRowData(response.data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const columnDefs = [
        { headerName: 'Date', field: 'date', sortable: true, filter: true, width: 350,  },
        { headerName: 'Purchase Id', field: 'purchase_id', sortable: true, filter: true, width: 400 },
        { headerName: 'View', field: 'view', 
            cellRenderer: (params) =>{
                return <a onClick={() => navigateToReceipt(params.data)} style={{color:'#046FAA',cursor:'pointer', textAlign:'center'}}>View</a>
            }
        },
    ];

    return (
        <div>
            <div>
                <div className='navigation_bar'>
                    <ul>
                        <li> <span style={{fontSize:"20px",color:"#046FAA", marginRight:"18px"}}><b>HarvestHub</b> <br/> <span style={{fontSize:"12px",padding:"0px",color:"#046FAA"}}>({name})</span></span></li>
                        <li style={{float:"right", color:"#046FAA"}} onClick={logout}><label>Logout</label></li>
                    </ul>
                </div>
            </div> <br/><br/>
            <div style={{padding:"10px", marginLeft:"25px"}}>
                    <button onClick={navigateToMenu} className='btn'><b>Menu</b></button>
            </div> <br/>
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
        </div>

    );
}

export default PurchaseHistory;