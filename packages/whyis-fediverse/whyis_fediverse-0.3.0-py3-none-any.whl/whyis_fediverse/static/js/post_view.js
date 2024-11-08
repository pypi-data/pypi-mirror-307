import {Vue, axios, createApp} from '../../../dist/whyis.js';
import post from './post.js';
import comment from './comment.js';
import newPost from './new_post.js';
import selections from './selections.js';

export default Vue.component('fedi-post-view', {
    name: "fedi-post-view",
    props:{
        object: {
            type: String,
            require: true
        }
    },
    data() {
        return {
            post: null,
            replies: null,
            loading: false,
            loadError: false,
            otherArgs: null,
        }
    },
    template: `
    <fedi-selection>
        <spinner :loading="loading" text='Loading...' v-if="loading"/>
        <div v-else class="md-layout md-gutter">
	    <div class="md-layout-item md-scrollbar">
	      <fedi-post v-if="post != null" 
                         v-bind:value="post">
              </fedi-post>
	    </div>
	    <div class="md-layout-item md-scrollbar">
              <div>
	        <md-empty-state
		    v-if="replies == null || replies.length == 0"
		    md-icon="forum"
                    md-label="Reply to this thread"
                    md-description="Reply below to continue this conversation.">
		</md-empty-state>
                <fedi-comment v-else
                           v-for="reply in replies"
                           :key="reply.id"
                           v-bind:value="reply">
                </fedi-comment>
	      </div>
              <fedi-new-post v-if="post != null"
                             :inReplyTo="post.id">
              </fedi-new-post>
            </div>
        </div>
    </fedi-selection>`,
    watch: {
    },
    components: {
    },
    methods: {
        async scrollBottom () {
//            if (Math.ceil(window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
//                await this.loadPage()
//            }
        },
	async loadPost() {
	    let response = await axios.get(`${ROOT_URL}about`,
					   {
					       params: {
						   view: "data",
						   uri: this.object
					       }
					   });
	    console.log(response.data);
	    this.post = response.data;
	},
	async loadReplies() {
            let response = await axios.get(`${ROOT_URL}about`,
				     {
					 params: {
					     view: "replies",
					     uri: this.object
					 }
				     });
	    this.replies = response.data;
	}
    },
    async mounted (){
        this.loading = true
        await Promise.all([this.loadPost(), this.loadReplies()])
        this.loading = false
        this.pollInterval = setInterval(this.loadReplies, 2000)
    },
    async unmounted() {
        window.removeEventListener("scroll", this.scrollBottom)
    }
})
