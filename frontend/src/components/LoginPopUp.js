import React from "react";

export const LoginPopUp = (props) =>
{
    const [email,setEmail] = React.useState("");
    const [password,setPassword] = React.useState("");
    const [errorMessage,setErrorMessage] = React.useState("");
  
    const switchToRegister = () =>{
        props.setOpenLoginModal(false)
        props.setOpenRegisterModal(true)
        }
    return(
            <div className="modal">
                <div  onClick={props.setOpenLoginModal.toggleLoginModal}  className="overlay">
                    <form className="login-pop-up-form">
                        <div>
                            <button onClick={props.setOpenLoginModal.toggleLoginModal} className="close-button">X</button>
                        </div>
                        <h1 className="form--title">Welcome back!</h1>
                        <div className="field" >
                            <label className="label">Email</label>
                            <div className="email--input"> 
                                <input type="email"
                                    placeholder="Email"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Password</label>
                            <div className="password--input">
                                <input type="password" 
                                   placeholder="Enter a password"
                                />
                            </div>
                        </div>
                        <button className="form--submit">
                          Sign in
                        </button>
                        <p className="text">
                            Don't have an account yet?{" "}
                            <button onClick={switchToRegister} className='button--link' >
                            Sign up
                            </button>
                        </p>
                    </form>
                </div>
            </div>
    )
}

export default LoginPopUp