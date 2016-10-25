import React from "react"
import ReactDOM from "react-dom"

const app = document.getElementById("react-reddit-app")

export default class RedditFinder extends React.Component {
    render() {
        return (
            <h1>Rendered with ReactJs (6)</h1>
        );
    }
}

ReactDOM.render(
    <RedditFinder/>,
    app
)