import React from "react"
import reachy_logo from "../images/reachy_logo4.png"
import RegisterPopUp from "./RegisterPopUp";
import LoginPopUp from "./LoginPopUp";
import { UserContext } from "../context/UserContext";


export default function Header(){

    const [registerModal, setRegisterModal] = React.useState(false);
    const [loginModal,setLoginModal] = React.useState(false);
    const [token,setToken] = React.useContext(UserContext);

    const toggleRegisterModal = () => {
        setRegisterModal(!registerModal)
    };

    const toggleLoginModal = ()=>{
        setLoginModal(!loginModal)
    };
    const handleLogout = () => {
        setToken(null);
      };


    return(
        <div>
        <header>
            <nav className="nav">
                <img  src={reachy_logo} className="logo_image" alt="logo"  />
                <h1>Reachy</h1>
                {!token ? (
                <div>
                    <ul className="nav-items">
                    <li>
                        <button className="button1" onClick ={toggleLoginModal}>Log in</button>
                    </li>
                    <li>
                        <button className="button2" onClick={toggleRegisterModal} >Sign up</button>
                    </li>
                    </ul>
                    {registerModal &&<RegisterPopUp setOpenRegisterModal={setRegisterModal} setOpenLoginModal={setLoginModal} />} 
                    {loginModal && <LoginPopUp setOpenLoginModal={setLoginModal} setOpenRegisterModal={setRegisterModal}/>}
                </div>
                ) : (
                    <div>
                        <ul className = "nav-items">
                            <li>
                                <button className="button3" onClick={handleLogout}>Log out</button>
                            </li>
                        </ul>
                    </div>
                )}
                </nav>
        </header> 
    </div>
    )
}