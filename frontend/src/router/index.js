import { createRouter, createWebHistory } from 'vue-router';
import Hello from '../components/HelloWorld.vue';
import Login from '../views/login.vue';
import Signup from '../views/signup.vue';
import adminlogin from '../views/adminlogin.vue';
import admindash from '../views/admindash.vue';
import subjectsview from '../views/subjectsview.vue';
import chapters from '../views/chapters.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: Hello },
        { path: '/login', name: 'login', component: Login },
        { path: '/signup', name: 'signup', component: Signup },
        { path: '/adminlogin', name: 'adminLogin', component: adminlogin },
        { path: '/admindash', name: 'admindash', component: admindash },
        { path: '/admindash/subjects', name: 'subjectview', component: subjectsview },
        { path: '/admindash/subject/:subject_id', name: 'chapters', component: chapters }
    ]
});

export default router;
