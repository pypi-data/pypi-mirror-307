import dayjs from '//unpkg.com/dayjs@1.11.13/esm';
import relativeTime from '//unpkg.com/dayjs@1.11.13/esm/plugin/relativeTime';
dayjs.extend(relativeTime);
import {Vue, axios, createApp} from '../../../dist/whyis.js';
export default Vue.component('fedi-comment', {
    name: "fedi-comment",
    props:{
        value: {
            type: Object,
            require: true
        },
	expanded: {
	    type: Boolean,
	    default: false
	}
    },
    data() {
        return {
            replies: [],
            loading: false,
            loadError: false,
            otherArgs: null,
            pageSize: 20,
        }
    },
    template: `
    <md-content style="margin-top:1.5em">
      <div v-if="value.attachment != null && value.attachment.length != 0">
        <img style="" v-for="image in value.attachment" :src="image.url" :alt="image.url">
      </div>
      <div style="width:fit-content; margin-top:0.5em; border-radius:1em; padding-left:0.75em; padding-right:0.75em; background-color:lightgray">
        <small>
          <a :href="value.attributedTo.view">
            <strong>{{value.attributedTo.name}}</strong>
            (@{{value.attributedTo.id.split('/').pop()}})
            {{published}}
          </a>
        </small>
        <div v-html="value.content"></div>
      </div>
    </md-content>
    `,
    watch: {
    },
    components: {
    },
    computed: {
	published: function() {
	    return dayjs(this.value.published).fromNow();
	},
	// a computed getter
	images: function () {
	    console.log(this.value.attachment);
	    // `this` points to the vm instance
	    let result = this.value.attachment.filter(function(x) {x.type.indexOf('Image') >= 0});
	    console.log(result);
	    return result;
	}
    },
    methods: {
        async loadPage() {
            // non-page sized results means we've reached the end.
            if (this.results.length % this.pageSize > 0)
                return
            const result = await axios.get(`${ROOT_URL}about`,
                                           { params: {
                                               view: "comments",
                                               uri: this.entity,
                                               limit: this.pageSize,
                                               offset: this.results.length
                                           }
                                           })
            this.results.push(...result.data)
        },
        async scrollBottom () {
            if (Math.ceil(window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
                await this.loadPage()
            }
        }
    },
    async mounted (){
    },
    async unmounted() {
    },
    created(){
    }
})
