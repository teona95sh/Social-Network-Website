import React from "react";

export const UserContext = React.createContext()

export const UserProvider = (props) =>{
    const [token,setToken] = React.useState(localStorage.getItem("UserToken"))

    React.useEffect(() =>{
        const fetchUser = async () => {
            const requestOptions = {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + token,
                },
            };   
            const response = await fetch ("http://localhost:8000/user/me");
            if(!response.ok) {
                setToken(null);
            }
            localStorage.setItem("UserToken", token);
        };
        fetchUser();
    }, [token]);
    return (
        <UserContext.Provider value = {[token,setToken]}>
            {/* Render props.children, allowing components to be placed inside the provider */}
            {props.children}
        </UserContext.Provider>
    )
}