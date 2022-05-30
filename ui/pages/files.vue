<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">

          <h2 class="title has-text-centered">Files</h2>
          <div class="file-list">

            <li v-for="item in files">
              {{ item.filename }} - {{ item.path }}
            </li>

          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Notification from '~/components/Notification';

export default {
  components: {
    Notification,
  },

  data() {
    return {
      files: [],
      error: null
    };
  },

  methods: {
    async getFiles() {
      this.$axios.get('/api/files/').then((response) => {
        this.files = response.data.files
      })
      .catch((e) => {
        console.log(e);
        this.error = e.response.data.message;
      })
    },
  },

  beforeMount(){
    this.getFiles();
  },
};
</script>
