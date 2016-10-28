import axios from "axios"
import React from "react"
import moment from "moment"
import { observer } from "mobx-react"

import { Reddit } from "../componets/RedditStore"

window.moment = moment

@observer
export default class RedditFinder extends React.Component {
    find() {
        const { subreddit, from_dt, to_dt, keyword }= this.props.store
        let params = {
            subreddit: subreddit
        }
        if (from_dt) {
            params['from'] = from_dt.unix()
        }
        if (to_dt) {
            params['to'] = to_dt.unix()
        }
        if (keyword) {
            params['keyword'] = keyword
        }

        this.props.store.loading = true
        axios.get("/items", {
            params: params
        })
            .then(response => {
                console.log("got response")
                this.props.store.clearAllReddits()
                console.log("cleared old data from store")
                response.data.items.map(item => {
                    this.props.store.addReddit(new Reddit(item))
                })
                console.log("populated store")
                this.props.store.loading = false
            })
            .catch(error => {
                if (error.response) {
                    console.log(`/items endpoint error ${error.response.status}: ${error.response.data}`)
                } else {
                    console.log(`Error processing /items endpoint. ${error.message}`)
                }
                this.props.store.loading = false
            })
    }

    _storeInput(field, value) {
        this.props.store[field] = value
    }
    subreddit(e) {
        this._storeInput("subreddit", e.target.value)
    }
    keyword(e) {
        this._storeInput("keyword", e.target.value)
    }
    from(e) {
        const { format } = this.props
        let dt = moment(e.target.value)
        this._storeInput("from_dt", dt)
    }
    to(e) {
        const { format } = this.props
        let dt = moment(e.target.value, format)
        this._storeInput("to_dt", dt)
    }

    render() {
        const { format } = this.props
        const { subreddit, from_dt, to_dt, keyword, reddits, loading } = this.props.store
        // leave dt as is if empty string (false)
        let from = from_dt && from_dt.format(format)
        let to = to_dt && to_dt.format(format)

        const redditList = reddits.map( reddit => (
            <li key={reddit.id}>
                <span>{reddit.content}</span>
            </li>
        ))

        return (
            <div>
                <h3>Search cached reddit</h3>
                <label htmlFor="find-in-subreddit">subreddit: </label>
                <input id="find-in-subreddit" value={subreddit} onChange={this.subreddit.bind(this)}/>
                <label htmlFor="find-in-from">from: </label>
                <input id="find-in-from" type="datetime-local" value={from} onChange={this.from.bind(this)}/>
                <label htmlFor="find-in-to">to: </label>
                <input id="find-in-to" type="datetime-local" value={to} onChange={this.to.bind(this)}/>
                <label htmlFor="find-in-keyword">keyword: </label>
                <input id="find-in-keyword" value={keyword} onChange={this.keyword.bind(this)}/>
                <button id="find-search" className="btn btn-primary" onClick={this.find.bind(this)}>Search</button>
                <span id="find-loader" style={{display: loading ? "auto" : "none"}}>fetching...</span>
                <ul>{redditList}</ul>
            </div>
        )
    }
}