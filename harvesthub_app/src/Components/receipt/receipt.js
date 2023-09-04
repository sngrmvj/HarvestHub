
import './receipt.css';
import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { GET_RECEIPT } from '../../constants';


const Receipt = () => {

    const navigate = useNavigate();
    const [data, setData] = useState();
    const [purchaseID, setPurchaseID] = useState();
    const [name, setName] = useState(localStorage.getItem('fullname'));
    const {state} = useLocation();
    const [isHidden, setIsHidden] = useState(false);

    const navigateToMenu = () => {
        navigate('/menu');
    }

    const navigateToOrderHistory = () => {
        navigate('/history');
    }

    const logout = () =>{
        localStorage.setItem('isLoggedIn',false);
        localStorage.removeItem('email');
        localStorage.removeItem('fullname');
        navigate("/")
    }

    useEffect(() => {

        let loginCheck = localStorage.getItem('isLoggedIn');
        if(loginCheck === 'false'){
            navigate("/");
        }

        if (state != null){
            const { data, commodity } = state;
            setTimeout(() => {
                if(window.location.pathname === "/receipt"){
                    setPurchaseID(data)
                    get_receipt(data, commodity)
                }
            }, "15000");
        }
        else{
            navigate("/history")
        }
        
    }, [state]);

    const get_receipt = async(id, commodity) => {
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

        let response = await fetch(`${GET_RECEIPT}?id=${id}&commodity=${commodity}`, options);
        let result = await response.json();
        if ('error' in result){
            toast.error(result.error)
        } else{
            setData(<div className='container'>
                    <div>
                        <div>
                            <p><b>Purchase ID</b></p>
                            <p>{result.data[0]['purchase_id']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Email</b></p> 
                            <p>{result.data[0]['email']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Commodity</b></p> 
                            <p>{result.data[0]['commodities']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Price</b></p> 
                            <p>{result.data[0]['price']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Weight</b></p> 
                            <p>{result.data[0]['weight']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Address</b></p>
                            <p>{result.data[0]['address']}</p>
                        </div> <br/>
                        <div>
                            <p><b>Date</b></p>
                            <p>{result.data[0]['date']}</p>
                        </div> <br/>

                    </div>
                </div>
            );
            document.getElementById('loader').style.display='none';
        }
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
            <div>
                <div style={{padding:"10px", marginLeft:"25px", float:"left"}}>
                    <button onClick={navigateToMenu} className='btn'><b>Menu</b></button>
                    <button onClick={navigateToOrderHistory} className='btn' style={{marginLeft:'10px'}}><b>Order History</b></button>
                </div> 
                <div style={{marginLeft:"300px", padding:"10px"}}>
                    <div id="loader" className="loader"></div>
                </div>
            </div><br/><br/>

            <div>{data}</div> 
        </div>
    );
};

export default Receipt;