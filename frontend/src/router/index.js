import { createRouter, createWebHistory } from 'vue-router';
import Hello from '../components/HelloWorld.vue';
import Login from '../views/LoginView.vue';
import Signup from '../views/SignupView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: Hello },
        { path: '/login', name: 'login', component: Login },
        { path: '/signup', name: 'signup', component: Signup }
    ]
});

export default router;
