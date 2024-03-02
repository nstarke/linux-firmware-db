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

let refresh = localStorage.getItem('refresh');
if (refresh) {
    refresh = parseInt(refresh);
} else {
    refresh = 0;
}

// const current = (new Date()).getTime();
// const day = 60 * 60 * 24 * 1000;

// if ((current - refresh) > day) {
//     localStorage.clear();
//     localStorage.setItem('refresh', (new Date()).getTime());
// }

let app = createApp(App);
app.use(router);
app.mount('#app')
