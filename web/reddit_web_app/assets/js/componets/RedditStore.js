import { observable } from "mobx"

export class Reddit {
    id
    author
    reddit_type
    subreddit
    created
    content // title or text

    constructor(reddit) {
        this.id = reddit.id
        this.author = reddit.author.name
        this.reddit_type = reddit.type
        this.subreddit = reddit.subreddit
        this.created = reddit.created
        this.content = this.reddit_type === 'submission' ? reddit.title : reddit.text
    }
}

export class RedditStore {
    @observable subreddit = "python"
    @observable from_dt = ""
    @observable to_dt = ""
    @observable keyword = ""
    // very poor performance if we make this observable; and no need for that, this does not change outside of RedditFinder.find()
    reddits = []

    @observable loading = false
    highlightBy = []

    addReddit(reddit) {
        this.reddits.push(reddit)
    }

    clearAllReddits() {
        // this.reddits.replace([])
        this.reddits = []
    }
}

export default new RedditStore