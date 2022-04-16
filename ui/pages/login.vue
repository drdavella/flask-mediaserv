<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Login!</h2>

          <Notification :message="error" v-if="error"/>

          <form method="post" @submit.prevent="login">

            <div class="field">
              <label class="label">Username</label>

              <div class="control">
                <input
                  type="text"
                  class="input"
                  name="username"
                  v-model="username"
                  required
                >
              </div>
            </div>

            <div class="field">
              <label class="label">Password</label>

              <div class="control">
                <input
                  type="password"
                  class="input"
                  name="password"
                  v-model="password"
                  required
                >
              </div>
            </div>

            <div class="control">
              <button type="submit" class="button is-dark is-fullwidth">Login</button>
            </div>
          </form>

          <div class="has-text-centered" style="margin-top: 20px">
            Need to create an account? <nuxt-link to="/register">Create New Account</nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Notification from '~/components/Notification';

export default {
  middleware: 'guest',

  components: {
    Notification,
  },

  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },

  methods: {
    async login() {
      try {
        await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password,
          },
        });

        this.$router.push('/');
      } catch (e) {
        console.log(e);
        this.error = e.response.data.message;
      }
    },
  },
};
</script>
