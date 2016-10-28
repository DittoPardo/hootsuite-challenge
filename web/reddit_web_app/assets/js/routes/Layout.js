import React from "react"
import RedditFinder from "./RedditFinder"

const DateTimeFormat = "YYYY-MM-DDTHH:mm"

export default class Layout extends React.Component {
    render() {
        return (
            <div>
                <RedditFinder store={this.props.store} format={DateTimeFormat}/>
            </div>
        )
    }
}