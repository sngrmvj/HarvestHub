import React, { useState, useEffect } from 'react';
import { DELETE_ITEM_IN_CART } from '../../constants';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './cart.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Cart = () => {
    const [groceries, setGroceries] = useState([]);
    const [totalWeight, setTotalWeight] = useState(0);
    const [totalPrice, setTotalPrice] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch grocery details from the backend API
        // Replace 'your_backend_endpoint' with the actual API endpoint
        fetch('your_backend_endpoint')
            .then(response => response.json())
            .then(data => {
                // Assuming data is a dictionary with grocery details
                setGroceries(data.items);
                calculateTotals(data.items);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, []);


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


        axios.delete(`${DELETE_ITEM_IN_CART}?commodity=${itemToRemove}`, options)
        .then(res => {
            if (res.status === 200) {
                toast.success(`${itemToRemove} is removed from the cart`)
            }
        })
        .catch(error => {
            toast.error("Check credentials")
        })
        setGroceries(updatedCart);
    };

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
            <div style={{padding:"20px"}}>
                <header style={{color:"#2E8DCD", fontSize:"20px"}}><b>HarvestHub</b></header>
            </div><br/><br/>

            <div style={{padding:"10px", marginLeft:"25px"}}>
                    <button onClick={navigateToMenu} className='btn'><b>Menu</b></button>
            </div> <br/><br/>

            <div className='cart-container'>
                <header className="cart-header"><b>Cart</b></header>
                <ul className="cart-list">
                    {groceries.map(item => (
                        <li key={item.id} className="cart-item">
                            <div className="cart-item-details">
                                <p className="cart-item-name">{item.name}</p>
                                <p className="cart-item-weight-price">
                                    Weight: {item.weight} kg, Price: {item.price} Rs
                                </p>
                                <button onClick={() => removeFromCart(item)}>Remove</button>
                            </div>
                        </li>
                    ))}
                </ul>
                <div className="cart-totals">
                    <p className="cart-total-label">Total Weight:</p>
                    <p className="cart-total-value">{totalWeight} kg</p>
                </div>
                <div className="cart-totals">
                    <p className="cart-total-label">Total Price:</p>
                    <p className="cart-total-value">{totalPrice} Rs</p>
                </div> <br/>
                <div>
                    <button className='btn'><b>Purchase</b></button>
                </div>
            </div>
        </div>
    );
}

export default Cart;