import {Vue, axios, createApp} from '../../../dist/whyis.js';

export default Vue.component('fedi-selectable', {
    name: "fedi-selectable",
    props : {
        "uri": String
    },
    inject : ['selection'],
    data : function() {
        return {
            "hover" : false,
        }
    },
    template : `
    <div style="margin: 0.5rem"
         v-on:click="toggle()"
         v-on:mouseenter="hover=true"
         v-on:mouseleave="hover=false"
         v-bind:class="{ selected: selected, hover: hover }" >
      <slot></slot>
    </div>
    `,
    computed : {
        selected : function() {
            return this.selection.includes(this.uri)
        }
    },
    methods: {
        toggle: function () {
            console.log("toggle",this.uri);
            console.log(this.selection)
            console.log(this.selection.includes(this.uri))
            if (this.selection.includes(this.uri)) {
                var index = this.selection.indexOf(this.uri)
                this.selection.splice(index, 1)
            } else {
                this.selection.push(this.uri)
            }
        },
    },
})
