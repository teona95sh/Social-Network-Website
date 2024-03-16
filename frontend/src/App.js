import React from "react"
import Header from "./components/Header"
import Main from "./components/Main"
import { UserContext } from "./context/UserContext"

export default function App(){
  return(
      <div className="container">
        <Header/>
        <Main/>
      </div>
  )
}