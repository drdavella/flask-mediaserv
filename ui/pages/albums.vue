<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">

          <h2 class="title has-text-centered">Albums</h2>
          <div class="album-list">

            <li v-for="item in albums">
              {{ item.name }} - {{ item.artist}}
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
      albums: [],
      error: null
    };
  },

  methods: {
    async getAlbums() {
      this.$axios.get('/api/albums/').then((response) => {
        this.albums = response.data.albums
      })
      .catch((e) => {
        console.log(e);
        this.error = e.response.data.message;
      })
    },
  },

  beforeMount(){
    this.getAlbums();
  },
};
</script>
