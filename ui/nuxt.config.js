export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  server: {
    host: 0
  },
  head: {
    title: 'media-frontend',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/bootstrap
    'bootstrap-vue/nuxt',
    'nuxt-buefy',
    '@nuxtjs/vuetify',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],

  auth: {
    strategies: {
      local: {
        token: {
          property: 'token',
          global: true,
        },
        endpoints: {
          login: {url: '/api/login/', method: 'post'},
          user: {url: '/api/user/', method: 'get'}
        }
      }
    }
  },

  axios: {
    proxy: true
  },

  vuetify: {
    defaultAssets: { icons: 'fa' }
  },

  proxy: {
    '/api/': process.env.API_URI || 'http://localhost:5000/'
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  },

  env: {
    apiUri: process.env.API_URI || 'http://localhost:5000/',
    websocketUri: process.env.WEBSOCKET_URI || 'wss://localhost:5000/'
  }
}
