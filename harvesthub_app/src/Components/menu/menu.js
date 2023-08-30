import './menu.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { GET_COMMODITIES, ADD_TO_CART } from '../../constants.js';



const Menu = () => {

    const navigate = useNavigate();
    const [name, setName] = useState(localStorage.getItem('fullname'));
    const [quantity, setQuantity] = useState();

    const navigateToCart = () =>{
        navigate("/cart");
    }

    const navigateToOrderHistory = () => {
        navigate("/history");
    }

    const logout = () =>{
        localStorage.setItem('isLoggedIn',false);
        localStorage.removeItem('email');
        navigate("/")
    }

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


    const add_to_cart = (item, price) =>{
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
                item: item,
                price: price,
                quantity: quantity,
                cost: price * quantity
            }
        };

        axios.put(`${ADD_TO_CART}`, options) // if promise get you success, control enters .then
        .then(res => {
            if (res.status === 200) {
                toast.success("Added to the cart")
                setQuantity('');
            }
        })
        .catch(error => {
            toast.error(`Error in adding the item to the cart - ${error}`)
        })
    }

    return(
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
                    <button onClick={navigateToCart} className='btn'><b>Cart</b></button>
                    <button onClick={navigateToOrderHistory} className='btn' style={{marginLeft:"10px"}}><b>Order History</b></button>
            </div> <br/><br/>

            <div style={{display:"flex", flexDirection:"row", padding:"20px"}}>
                {
                    commodtites.map((commodity, i) => (
                        <div key={i} style={{padding:"20px", borderRadius:"5px", boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)", margin:"10px"}}>
                            <p><b>Item</b></p>
                            <p>{commodity[0]}</p> <br/>
                            <p><b>Price/kg</b> </p>
                            <p>{commodity[1]}</p> <br/>
                            <p><b>Enter the weight</b> (kg)</p>
                            <input type='number' onChange={(e) => setQuantity(e.target.value)}/> <br/><br/>
                            <button className='btn' style={{padding:"10px"}} onClick={(e) => add_to_cart(commodity[0], commodity[1])}><b>Add to cart</b></button>
                        </div>
                    ))
                }
            </div>

            <ToastContainer />
        </div>
    );
}


export default Menu;