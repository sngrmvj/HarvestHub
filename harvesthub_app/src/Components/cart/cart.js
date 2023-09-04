import React, { useState, useEffect } from 'react';
import { DELETE_ITEM_IN_CART, GET_CART, PURCHASE_ORDER, VALIDATE_USER } from '../../constants';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './cart.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Cart = () => {
    const [groceries, setGroceries] = useState([]);
    const [totalWeight, setTotalWeight] = useState(0);
    const [totalPrice, setTotalPrice] = useState(0);
    const [name, setName] = useState(localStorage.getItem('fullname'));
    const navigate = useNavigate();


    useEffect(() => {
        // Fetch grocery details from the backend API
        // Replace 'your_backend_endpoint' with the actual API endpoint
        let email = localStorage.getItem('email')
        fetch(`${GET_CART}?email=${email}`)
            .then(response => response.json())
            .then(data => {
                // Assuming data is a dictionary with grocery details
                setGroceries(data.data);
                calculateTotals(data.data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const logout = () =>{
        localStorage.setItem('isLoggedIn',false);
        localStorage.removeItem('email');
        localStorage.removeItem('fullname');
        navigate("/")
    }


    const navigateToMenu = () =>{
        navigate('/menu');
    }

    // Remove item from the cart
    const removeFromCart = (itemToRemove) => {
        const updatedCart = groceries.filter(item => item !== itemToRemove);
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

        let email = localStorage.getItem('email')
        axios.delete(`${DELETE_ITEM_IN_CART}?commodity=${itemToRemove}&email=${email}`, options)
        .then(res => {
            if (res.status === 200) {
                toast.success(res.data.message);
                setGroceries(res.data.data);
            }
        })
        .catch(error => {
            toast.error(`Error in removal of the item from cart - ${error}`);
        })
        setGroceries(updatedCart);
    };


    const purchase_order = () => {
        const options = {
            withCredentials: true,
            credentials: 'same-origin',

            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                'Content-Type': 'application/json',
            },

            data : {
                commodities: groceries,
            }
        };
        let email = localStorage.getItem('email')
        axios.put(`${PURCHASE_ORDER}?email=${email}`, options)
        .then(res => {
            if (res.status === 200) {
                toast.success(`Successfully purchased the order`)
                navigate("/menu");
            }
        })
        .catch(error => {
            toast.error(`Error in purchasing the order ${error}`)
        })
    }


    const calculateTotals = (groceries) => {
        let totalWeight = 0;
        let totalPrice = 0;

        groceries.forEach(item => {
            totalWeight += item.weight;
            totalPrice += item.price;
        });

        setTotalWeight(totalWeight);
        setTotalPrice(totalPrice);
    };

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
            </div> <br/><br/>

            <div>
                {
                    groceries ? <div className='cart-container'>
                        <header className="cart-header"><b>Cart</b></header>
                        <div style={{ listStyle: "none", padding: 0 }}>
                            {groceries.map((item, i) => (
                                <div key={i} className='li' style={{ padding: "10px", display: "flex", flexDirection:"row", justifyContent: "space-between",  borderBottom: "1px solid #ccc" }}>
                                    <div>
                                        <p><b>Commodity</b></p>
                                        <p>{item['commodity']}</p><br />
                                        <p><b>Weight</b></p>
                                        <p>{item['weight']}</p><br />
                                        <p><b>Price</b></p>
                                        <p>INR {item['price']}</p><br />
                                    </div>
                                    <div>
                                        <button style={{ border: "none", backgroundColor: "transparent", color: "#2E8DCD", cursor: "pointer", marginTop:"20px" }} onClick={() => removeFromCart(item['commodity'])}><b>Remove</b></button>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="cart-totals">
                            <p className="cart-total-label">Total Weight:</p>
                            <p className="cart-total-value">{totalWeight} kg</p>
                        </div>
                        <div className="cart-totals_below">
                            <p className="cart-total-label">Total Price:</p>
                            <p className="cart-total-value">INR {totalPrice}</p>
                        </div> <br/>
                        <div>
                            <button className='btn' onClick={purchase_order}><b>Purchase</b></button>
                        </div>
                    </div>: <span style={{padding:"35px", color:'#046FAA', fontWeight:"bold"}}><span className='cart-container'>No Items added yet</span></span>
                }
            </div>
            <br/><br/><br/>

            <ToastContainer />
        </div>
    );
}

export default Cart;