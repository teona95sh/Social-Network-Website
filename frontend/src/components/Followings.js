import React, { useContext, useEffect, useState } from "react";

const Followings = ({ active, handleModal, token, setErrorMessage }) => {

  const [name, setName] = useState("");

  useEffect(() => {
    const getFollowings = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      };
      const response = await fetch(`http://localhost:8000/follow/followings_list`, requestOptions);

      if (!response.ok) {
        setErrorMessage("Could not get the followings");
      } else {
        const data = await response.json();
        setName(data.name);
      }
    };
  }, [token]);
}
