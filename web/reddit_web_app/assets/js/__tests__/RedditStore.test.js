import _ from "lodash"
// import the store class rather than module created object
import { RedditStore, Reddit } from "../componets/RedditStore"


describe("RedditStore", () => {
    const input_reddits = [
        {
            id: 'submission_1',
            author: {name: 'auth_1'},
            type: 'submission',
            subreddit: 'python',
            created: 12345678,
            title: 'a title',
        },
        {
            id: 'comment_1',
            author: {name: 'auth_2'},
            type: 'comment',
            subreddit: 'python',
            created: 22345678,
            text: 'a text',
        }
    ]

    it("creates new reddit objects", () => {
        const store = new RedditStore()
        const inputs = _.cloneDeep(input_reddits)
        const inputs_r = inputs.map( r => new Reddit(r))
        inputs_r.map( r => store.addReddit(r))
        expect(store.reddits.length).toBe(2)
        expect(store.reddits[0].id).toBe(inputs[0].id)
        expect(store.reddits[0].author).toBe(inputs[0].author.name)
        expect(store.reddits[0].reddit_type).toBe(inputs[0].type)
        expect(store.reddits[0].content).toBe(inputs[0].title)
    })

    it("clears the store of reddits", () => {
        const store = new RedditStore()
        store.reddits.push(1)
        expect(store.reddits.length).toBe(1)
        store.clearAllReddits()
        expect(store.reddits.length).toBe(0)
    })
})