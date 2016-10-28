import React from "react"
import ReactDOM from "react-dom"
import RedditStore from "./componets/RedditStore"
import Layout from "./routes/Layout"

const app = document.getElementById("react-reddit-app")

ReactDOM.render(
    <Layout store={RedditStore}/>,
    app
)