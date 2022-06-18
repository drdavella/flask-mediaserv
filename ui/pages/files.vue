<template>
  <v-app>
    <v-layout row>
      <v-flex xs12 sm6 offset-sm3>
        <v-card class="mx-auto">
          <v-toolbar color="blue" dark>
            <v-toolbar-side-icon></v-toolbar-side-icon>

            <v-toolbar-title>Files</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon>
              <v-icon>fa-search</v-icon>
            </v-btn>

            <v-btn icon>
              <v-icon>fa-bars</v-icon>
            </v-btn>
          </v-toolbar>

          <v-list no-border one-line>
            <v-list-item
              v-for="item in files"
              :key="item.filename"
              avatar
              @click=""
            >
              <v-list-item-avatar>
                <v-icon>fas fa-music</v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{ item.name }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-flex>
    </v-layout>
  </v-app>
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
      path: "",
      error: null
    };
  },

  methods: {
    async getFiles() {
      this.$axios.get('/api/files/').then((response) => {
        this.files = response.data.files
        this.path = response.data.path
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
