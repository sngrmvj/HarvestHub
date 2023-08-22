



import './signup.css';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { SIGNUPURL } from '../../constants';


const Signup = () => {

    const navigate = useNavigate();
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [selectedOption, setSelectedOption] = useState('');

    useEffect(() => {
        if(localStorage.getItem('isLoggedIn') === "true"){
            navigate("/exercises");
        }
    });

    const handleOptionChange = (event) => {
        setSelectedOption(event.target.value);
    };


    const navigateToLogin = () => {
        navigate("/");
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // Perform registration here
        var data = {
            email: email,
            password: password,
            username: name,
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

        axios.post(`${SIGNUPURL}?type=${selectedOption}`, options)
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
            </div><br/>

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


                                <div>
                                    <label className="container" style={{fontSize:"18px"}}>Supplier
                                        <input type="radio"
                                            value="Supplier"
                                            checked={selectedOption === 'Supplier'}
                                            onChange={handleOptionChange}
                                        />
                                        <span className="checkmark"></span>
                                    </label><br/>
                                    <label className="container" style={{fontSize:"18px"}}>Consumer
                                        <input type="radio"
                                            value="Consumer"
                                            checked={selectedOption === 'Consumer'}
                                            onChange={handleOptionChange}
                                        />
                                        <span className="checkmark"></span>
                                    </label>
                                </div> <br/><br/>

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