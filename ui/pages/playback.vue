<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">

          <h2 class="title has-text-centered">Playback</h2>
          <div class="playback-status">

            <p>Time: {{ timestamp }}</p>

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
      timestamp: 0,
      error: null
    };
  },

  methods: {
    async setupPlayback() {
      try {
        console.log("Starting connection to WebSocket Server")
        this.connection = new WebSocket(process.env.websocketUri + '/api/playback/status/')

        let vue_this = this
        this.connection.onmessage = function(event) {
          console.log(event);
          vue_this.timestamp = event.data
        }

        this.connection.onopen = function(event) {
          console.log(event)
          console.log("Successfully connected to the echo websocket server...")
        }
      } catch (e) {
        console.log(e)
      }
    },
  },

  beforeMount(){
    this.setupPlayback();
  },
};
</script>
