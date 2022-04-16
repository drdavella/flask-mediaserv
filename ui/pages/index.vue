<template>
  <div class="search">
    <p>Hello there!</p>
    <b-field label="Search">
      <b-input class="search-box" @input="update"></b-input>
    </b-field>
    <p>Footer {{ data }}</p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { debounce } from 'lodash'
const axios = require('axios')

export default Vue.extend({
  name: 'IndexPage',
  data: () => ({
    data: ''
  }),
  methods: {
    update: debounce(function (this: any, value: any) {
      if (value) {
        console.log(value)
        this.data = value

        /* This is hacky but seems to be required by the flask router */
        let search = encodeURIComponent(encodeURIComponent(value))
        this.$axios.get('/api/search/' + search)
          .then(function (response) {
            console.log(response)
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    }, 100)
  }
})
</script>
