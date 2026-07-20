// Purpose: Entry point for the Vue application. It creates the app, connects the router, and mounts Vue to index.html.
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Create the Vue app using App.vue as the root component.
const app = createApp(App)

// Register Vue Router so <RouterLink> and <RouterView> work.
app.use(router)

// Mount the Vue app inside the <div id="app"></div> in index.html.
app.mount('#app')
