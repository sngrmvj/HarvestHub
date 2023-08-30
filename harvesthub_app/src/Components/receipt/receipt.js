
import './receipt.css';
import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { GET_RECEIPT } from '../../constants';


const Receipt = () => {

    const navigate = useNavigate();
    const [data, setData] = useState();
    const [purchaseID, setPurchaseID] = useState();
    const [name, setName] = useState(localStorage.getItem('fullname'));
    const {state} = useLocation();

    const navigateToMenu = () => {
        navigate('/menu');
    }

    const navigateToOrderHistory = () => {
        navigate('/history');
    }

    const logout = () =>{
        localStorage.setItem('isLoggedIn',false);
        localStorage.removeItem('email');
        navigate("/")
    }

    useEffect(() => {
        let loginCheck = localStorage.getItem('isLoggedIn');
        if(loginCheck === 'false'){
            navigate("/");
        }

        if (state != null){
            const { id } = state;
            setPurchaseID(id)
            get_receipt()
        }
        else{
            navigate("/history")
        }
        
    }, [data]);

    const get_receipt = () => {
        axios.get(`${GET_RECEIPT}?id=${purchaseID}`)
        .then(response => {
            setData(response.data);
        })
        .catch(error => console.error('Error fetching data:', error));
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
                    <button onClick={navigateToMenu} className='btn'><b>Menu</b></button>
                    <button onClick={navigateToOrderHistory} className='btn' style={{marginLeft:'10px'}}><b>Order History</b></button>
            </div> <br/>
            <div className='container'>
                {/* <div>
                    <div>
                        <p>Purchase ID</p>
                        <p>{purchaseID}</p>
                    </div> <br/>
                    <div>
                        <p>Email</p>
                        <p>{data['email']}</p>
                    </div> <br/>
                    <div>
                        <p>Address</p>
                        <p>{data['address']}</p>
                    </div> <br/>
                    <div>
                        <p>Date</p>
                        <p>{data['date']}</p>
                    </div> <br/>
                    <div>
                        {
                            data['commodities'].map((commodity,i) => (
                                <div key={i} style={{padding:"20px", borderBottom:"1px solid black", margin:"10px"}}>
                                    <label style={{marginRight:"10px"}}>{commodity[0]}</label>
                                    <label style={{marginRight:"10px"}}>{commodity[1]}</label>
                                    <label style={{marginRight:"10px"}}>{commodity[2]}</label>
                                </div>
                            ))
                        }
                    </div> <br/>
                </div> */}
            </div>
        </div>
    );
};

export default Receipt;