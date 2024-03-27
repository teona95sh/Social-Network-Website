import React from "react";
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

export const Register = ({ switchToLogin })=> 
{    
    const [name,setName] = React.useState("");
    const [email,setEmail] = React.useState("");
    const [password,setPassword] = React.useState("");
    const [confirmationPassword,setConfirmationPassword] = React.useState("");
    const [errorMessage,setErrorMessage] = React.useState("");
    const [,setToken] = React.useContext(UserContext);

    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name:name, email: email, password: password}),
        };

        const response = await fetch ("http://localhost:8000/user/",requestOptions);
        const data = await response.json();
        console.log(data.access_token);
        if (!response.ok){
            setErrorMessage(data.detail)
        }
        else{
            setToken(data.access_token)
        }
    };

    const handleSubmit = (e) =>{
        e.preventDefault();
        if (password === confirmationPassword){
            submitRegistration();
        }
        else{
            setErrorMessage("Ensure that the password match");
        }
    };


   return(
        <div className="form-container">
                <form className="register-form" onSubmit={handleSubmit}>
                    <h1 className="form--title">Let's get started!</h1>
                    <div className="field" >
                        <label className="label">Email</label>
                        <div className="email--input"> 
                            <input type="email"
                                    placeholder="Enter email"
                                    value ={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                            />
                        </div>
                    </div>
                    <div  className="field">
                        <label className="label">Name</label>
                        <div className="name--input">
                            <input type="name"
                                   placeholder="Enter name"
                                   value={name}
                                   onChange={(e) => setName(e.target.value)}
                                   required
                            />
                        </div>
                    </div>
                    <div className="field">
                        <label className="label">Password</label>
                        <div className="password--input">
                            <input type="password" 
                                   placeholder="Create a password"
                                   value={password}
                                   onChange={(e) => setPassword(e.target.value)}
                                   required
                            />
                        </div>
                    </div>
                    <div className="field">
                        <label className="label">Confirm password</label>
                        <div className="password--input">
                            <input type="password" 
                                   placeholder="Confirm password"
                                   value={confirmationPassword}
                                   onChange={(e) => setConfirmationPassword(e.target.value)}
                                   required
                            />
                        </div>
                    </div>
                    <ErrorMessage message={errorMessage}/>
                    <br/>
                    <button className="form--submit" type ="submit"> 
                        Sign up
                    </button>
                    <p className="text">
                        Already have an account?{" "}
                       <button className='button--link' onClick={switchToLogin}>
                           Log in
                       </button>
                    </p>
                </form>
        </div>
    );
};

export default Register;