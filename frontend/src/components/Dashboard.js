import React from "react"
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

export const Dashboard = () =>
{
    const [token] =  React.useContext(UserContext);
    const [name,setName] = React.useState("");
    const [errorMessage, setErrorMessage] = React.useState("");

    const getUser = async () => {
        const requestOptions = {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
        };
        const response = await fetch("http://localhost:8000/user/me", requestOptions);
        if (!response.ok) {
            setErrorMessage("Could not get the user");
          } else {
            const data = await response.json();
            setName(data.name);
            console.log(data.name)
          }
        };
        React.useEffect(() => {
            getUser();
          }, []);
    
    return(
        <main>
            <h1>Welcome to Dashboard!</h1>
            <nav>
              <div className="LeftMenu">
                    <button className="button_MyProfile">My Profile</button>
                    <br />
                    <button className="button_friends">Friends</button>
                    <br />
                    <button className="button_followers">Followers</button>
                    <br />
                    <button className="button_followings">Followings</button>
                    <br />
                    <button className="button_notifications">Notifications</button>
                    <br />
              </div>
            </nav>
        </main>
    );
}


export default Dashboard;