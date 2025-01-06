import './assets/global.postcss'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { VueReCaptcha } from 'vue-recaptcha-v3';

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(VueReCaptcha, {
    siteKey: '6LeVnoYqAAAAAH-2XnunCXZYDd65_f93BwTt1Zzj', 
});

app.mount('#app')
