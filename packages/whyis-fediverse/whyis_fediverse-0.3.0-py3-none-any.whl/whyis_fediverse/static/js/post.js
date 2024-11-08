import dayjs from '//unpkg.com/dayjs@1.11.13/esm';
import relativeTime from '//unpkg.com/dayjs@1.11.13/esm/plugin/relativeTime';
dayjs.extend(relativeTime);


import selectable from './selectable.js';

import {Vue, axios, createApp} from '../../../dist/whyis.js';
export default Vue.component('fedi-post', {
    name: "fedi-post",
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
    <md-card>
      <md-card-header>
        <md-card-header-text>
          <div class="md-subhead">
            <a :href="value.attributedTo.view">
              <md-avatar class="md-avatar-icon">{{value.attributedTo.name[0]}}</md-avatar>
              <strong>{{value.attributedTo.name}}</strong> <small>(@{{value.attributedTo.id.split('/').pop()}})</small>
            </a>
            <br/>
            <small><a :href="value.view">{{published}}</a></small>
          </div>
          <div class="md-title" v-if="value.name"><a :href="value.id">{{value.name}}</a></div>
        </md-card-header-text>
      </md-card-header>
      <md-card-content v-html="value.content"></md-card-content>
      <md-card-media v-if="(value.attachment != null && value.attachment.length != 0) || (value.context != null && value.context.length != 0)">
        <fedi-selectable v-bind:uri="a.id" v-for="a in value.attachment" v-bind:key="a.id" v-html="a.embed">
        </fedi-selectable>
        <fedi-selectable v-bind:uri="a.id" v-for="a in value.context" v-bind:key="a.id" v-html="a.embed">
        </fedi-selectable>
      </md-card-media>
    </md-card>
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
