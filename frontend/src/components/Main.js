import React from "react"
import Register from "./Register"
import Login from "./Login";
import background_img from "../images/website-background2.jpg"

export default function Main(){
  const [activeForm, setActiveForm] = React.useState("register");

  const switchToLogin = () => {
    setActiveForm("login");
  };

  const switchToRegister = () => {
    setActiveForm("register");
  };
    return(
        <main>
            <h1 className="main--title">Welcome to Reachy – Connect, Share, Thrive!</h1>
            <img src={background_img} className="background_image" alt="background"  />
            {activeForm === "login" && <Login switchToRegister={switchToRegister} />}
            {activeForm === "register" && <Register switchToLogin={switchToLogin} />}
        </main>
    )
}