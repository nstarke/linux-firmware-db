import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import MainView from './components/MainView.vue'
import DisassemblyView from './components/DisassemblyView.vue'

const routes = [
    {
        path: "/",
        component: MainView,
        name: "main",
    },
    {
        path: "/disassembly/:sha256",
        component: DisassemblyView,
        name: "disassembly",
        props: true
    }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

let app = createApp(App);
app.use(router);
app.mount('#app')
