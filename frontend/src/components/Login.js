import React from "react"
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";


export const Login = ({switchToRegister}) => 
{
    const [email,setEmail] = React.useState("");
    const [password,setPassword] = React.useState("");
    const [errorMessage,setErrorMessage] = React.useState("");
    const [,setToken] = React.useContext(UserContext)

    const submitLogin = async () => {
        const requestOptions ={
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded" },
            body: JSON.stringify(
                `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
                ),
            };

        const response = await fetch ("http://localhost:8000/login", requestOptions);
        const data = await response.json();
        console.log(data.access_token)
        if(!response.ok){
            setErrorMessage(data.detail);
        } else {
            setToken(data.access_token);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    }
    return(
            <div className="form-container">
                <form className="login-form" onSubmit={handleSubmit}>
                    <h1 className="form--title">Welcome back!</h1>
                    <div className="field" >
                        <label className="label">Email</label>
                        <div className="email--input"> 
                            <input 
                              type="email"
                              placeholder="Enter email"
                              value={email}
                              onChange={(e) => setEmail(e.target.value)}
                              required
                            />
                        </div>
                    </div>
                    <div className="field">
                        <label className="label">Password</label>
                        <div className="password--input">
                            <input 
                              type="password" 
                              placeholder="Enter a password"
                              value={password}
                              onChange={(e)=> setPassword(e.target.value)}
                              required
                            />
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage} />
                    <button className="form--submit" type="submit"> 
                        Sign in
                    </button>
                    <p className="text">
                        Don't have an account yet?{" "}
                       <button className='button--link' onClick={switchToRegister}>
                           Sign up
                       </button>
                    </p>
                </form>
        </div>
    )
}

export default Login;