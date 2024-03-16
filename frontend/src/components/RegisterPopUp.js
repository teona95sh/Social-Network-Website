import React from "react";

export const RegisterPopUp = (props) => 
{
    const [name,setName] = React.useState("");
    const [email,setEmail] = React.useState("");
    const [password,setPassword] = React.useState("");
    const [confirmationPassword,setConfirmationPassword] = React.useState("");
    const [errorMessage,setErrorMessage] = React.useState("");
    const switchToLogin = () =>{
        props.setOpenRegisterModal(false)
        props.setOpenLoginModal(true)
        }
    return(
            <div className="modal">
                <div  className="overlay">
                    <form className="register-pop-up-form">
                        <div>
                            <button onClick={props.setOpenRegisterModal.toggleRegisterModal} className="close-button">X</button>
                        </div>
                        <h1 className="form--title">Let's get started!</h1>
                        <div className="field" >
                            <label className="label">Email</label>
                            <div className="email--input"> 
                                <input type="email"
                                    placeholder="Email"
                                />
                            </div>
                        </div>
                        <div  className="field">
                            <label className="label">Name</label>
                            <div className="name--input">
                                <input type="name"
                                   placeholder="Name"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Password</label>
                            <div className="password--input">
                                <input type="password" 
                                   placeholder="Create a password"
                                />
                            </div>
                        </div>
                        <button className="form--submit">
                          Sign up
                        </button>
                        <p className="text">
                            Already have an account?{" "}
                            <button onClick={switchToLogin} className='button--link' >
                            Log in
                            </button>
                        </p>
                    </form>
                </div>
            </div>
    )
}

export default RegisterPopUp;