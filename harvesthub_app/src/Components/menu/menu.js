import './menu.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import { AgGridReact } from 'ag-grid-react';
// import 'ag-grid-community/dist/styles/ag-grid.css';
// import 'ag-grid-community/dist/styles/ag-theme-alpine.css';
// import 'ag-grid-community/dist/styles/ag-theme-balham.css';
// import 'ag-grid-community/dist/styles/ag-theme-balham-dark.css';
// import 'ag-grid-community/dist/styles/ag-theme-alpine-dark.css';
// import 'ag-grid-community/dist/styles/ag-theme-material.css';
import 'react-toastify/dist/ReactToastify.css';
import { GET_COMMODITIES } from '../../constants.js';



const Menu = () => {

    const navigate = useNavigate();

    useEffect( () =>{
        let loginCheck = localStorage.getItem('isLoggedIn');
        if(loginCheck === 'false'){
            navigate("/");
        }
        fetch_the_commodities();
    })

    const [commodtites, setTheCommodtities] = useState([['Tomato', 120], ['Potato', 20]]);

    const fetch_the_commodities = () => {

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

        axios.get(`${GET_COMMODITIES}`) // if promise get you success, control enters .then
        .then(res => {
            if (res.status === 200) {
                setTheCommodtities(res.data)
            }
        })
        .catch(error => {
            toast.error("Check credentials")
        })
    }


    const add_to_cart = () =>{
        axios.get(`${GET_COMMODITIES}`) // if promise get you success, control enters .then
        .then(res => {
            if (res.status === 200) {
                setTheCommodtities(res.data)
            }
        })
        .catch(error => {
            toast.error("Check credentials")
        })
    }

    return(
        <div>
            <div style={{padding:"20px"}}>
                <header style={{color:"#2E8DCD", fontSize:"20px"}}><b>HarvestHub</b></header>
            </div><br/><br/><br/>
            <div style={{display:"flex", flexDirection:"row", padding:"20px"}}>
                {
                    commodtites.map((commodity) => (
                        <div style={{padding:"20px", borderRadius:"5px", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)", margin:"20px"}}>
                            <p><b>{commodity[0]}</b></p>
                            <p><b>Price/kg</b> - {commodity[1]}</p>
                            <button className='btn' style={{padding:"10px"}} onClick={add_to_cart}>Add to cart</button>
                        </div>
                    ))
                }
            </div>
        </div>
    );
}


export default Menu;