import React from "react"
import reachy_logo from "../images/reachy_logo4.png"
import RegisterPopUp from "./RegisterPopUp";
import LoginPopUp from "./LoginPopUp";

export default function Header(){

    const [registerModal, setRegisterModal] = React.useState(false);
    const [loginModal,setLoginModal] = React.useState(false);

    const toggleRegisterModal = () => {
        setRegisterModal(!registerModal)
    }

    const toggleLoginModal = ()=>{
        setLoginModal(!loginModal)
    }


    return(
        <header>
            <nav className="nav">
                <img  src={reachy_logo} className="logo_image" alt="logo"  />
                <h1>Reachy</h1>
                <ul className="nav-items">
                    <li>
                        <button className="button1" onClick ={toggleLoginModal}>Log in</button>
                    </li>
                    <li>
                        <button className="button2" onClick={toggleRegisterModal} >Sign up</button>
                    </li>
                </ul>
                {  registerModal &&<RegisterPopUp setOpenRegisterModal={setRegisterModal} setOpenLoginModal={setLoginModal} />} 
                { loginModal && <LoginPopUp setOpenLoginModal={setLoginModal} setOpenRegisterModal={setRegisterModal}/>}

            </nav>
        </header> 
    )
}