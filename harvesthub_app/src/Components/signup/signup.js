



import './signup.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { SIGNUPURL, VALIDATE_USER } from '../../constants';


const Signup = () => {

    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [address, setAddress] = useState("");
    const [phonenumber, setPhonenumber] = useState("");

    useEffect(() => {
        if(localStorage.getItem('isLoggedIn') === "true"){
            navigate("/menu");
        }
        // validAuthentication();
    });


    const navigateToLogin = () => {
        navigate("/");
    }

    // const validAuthentication = () => {
    //     axios.get(`${VALIDATE_USER}`)
    //     .then((res) => {
    //         navigate("/menu");
    //     })
    //     .catch((error) => {
    //         toast.error("User Autentication Failed");
    //     })
    // }

    const handleSubmit = (e) => {
        e.preventDefault();
        

        var data = {
            email: email,
            password: password,
            username: name,
            address: address,
            phonenumber: phonenumber
        }

        const options = {
            withCredentials: true,
            credentials: 'same-origin',

            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
                'Content-Type': 'application/json',
            },

            data : data
        };

        axios.post(`${SIGNUPURL}`, options)
        .then(result=>{
            if(result.status === 200){
                navigate("/");
            } else {
                toast.warn("Please check the inputs")
            }

        }).catch(error => {
            if (error.status === 404){
                toast.error("Error Not Found");
            } else {
                toast.error(error.error);
            }

        })
    };

    return (
        <span>
            <div style={{padding:"20px"}}>
                <header style={{color:"#2E8DCD", fontSize:"20px"}}><b>HarvestHub</b></header>
            </div><br/><br/><br/><br/>

            <span className='signupmain'>
                <div className='signupdiv'>
                    <div className='sidediv'>
                        <div style={{display:"block", padding:"10px", }}>
                            <label className='switchText' onClick={navigateToLogin}><b>Login</b></label>
                        </div><br/>
                        <div style={{display:"block", padding:"10px", }}>
                            <label style={{color:"#2E8DCD", borderBottom:"2px solid #2E8DCD", padding:"5px"}} ><b>Register</b></label>
                        </div>
                    </div>

                    <div style={{display:"flex",flexDirection:"column", padding:"20px"}}>
                        <div style={{display:"flex",flexDirection:"column", padding:"20px"}}>

                            <header className='signUpheader'>Register</header> <br/><br/>
                            <form onSubmit={handleSubmit}>
                                <label htmlFor="email">Fullname:</label><br/>
                                <input
                                    type="text"
                                    id="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                /><br/><br/>


                                <label htmlFor="email">Email:</label><br/>
                                <input
                                    type="email"
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                /><br/><br/>

                                <label htmlFor="password">Password:</label><br/>
                                <input
                                    type="password"
                                    id="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                /><br/><br/>

                                <label htmlFor="address">Address:</label><br/>
                                <textarea
                                    id="address"
                                    rows="5"
                                    cols="50"
                                    value={address}
                                    onChange={(e) => setAddress(e.target.value)} />
                                <br/><br/>

                                <label htmlFor="tel">Phone number:</label><br/>
                                <input
                                    type="number"
                                    id="number"
                                    pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
                                    value={phonenumber}
                                    maxLength="10" minLength="10"
                                    onChange={(e) => setPhonenumber(e.target.value)}
                                /><br/><br/>

                                <button type="submit" className='btn'>Register</button><br/><br/>
                            </form>
                        </div>
                    </div>
                </div>
            </span>


            <ToastContainer />
        </span>
    );
};


export default Signup;