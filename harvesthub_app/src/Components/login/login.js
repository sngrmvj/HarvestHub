


import './login.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import React from 'react';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { LOGINURL } from '../../constants.js';



const Login = () => {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    useEffect(() => {
        if(localStorage.getItem('isLoggedIn') === "true"){
            navigate("/menu")
        }
    },[]);


    const navigateToSignUp = () => {
        navigate("/register");
    };

    const handleSubmit = (e) => {
        e.preventDefault();

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
                email: email,
                password: password,
            }
        };

        axios.put(`${LOGINURL}`, options) // if promise get you success, control enters .then
        .then(res => {
            if (res.status === 200) {
                localStorage.setItem('isLoggedIn',true);
                localStorage.setItem('fullname', res.data.fullname);
                localStorage.setItem('email', res.data.email)
                navigate("/menu");
            }
        })
        .catch(error => {
            toast.error("Check credentials")
        })

    };

    return (

        <span>
            <div style={{padding:"20px"}}>
                <header style={{color:"#2E8DCD", fontSize:"20px"}}><b>HarvestHub</b></header>
            </div><br/><br/><br/>

            <span className='main'>
                <div className='maindiv'>
                    <div className='sidediv'>
                        <div style={{display:"block", padding:"10px", }}>
                            <label style={{color:"#2E8DCD", borderBottom:"2px solid #2E8DCD", padding:"5px"}} ><b>Login</b></label>
                        </div> <br/>
                        <div style={{display:"block", padding:"10px", }}>
                            <label className='switchText' onClick={navigateToSignUp}><b>Register</b></label>
                        </div>
                    </div>

                    <div style={{display:"flex",flexDirection:"column", padding:"20px"}}>
                        <div style={{display:"flex",flexDirection:"column", padding:"20px"}}>

                            <header className='header'>Login</header> <br/><br/>
                            <form onSubmit={handleSubmit}>
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

                                <button type="submit" className='btn'>Login</button><br/><br/>

                            </form>
                        </div>

                    </div>
                </div>
            </span>

            <ToastContainer />
        </span>

    );
};


export default Login;