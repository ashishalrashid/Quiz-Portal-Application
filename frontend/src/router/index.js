import { createRouter, createWebHistory } from 'vue-router';
import Hello from '../components/HelloWorld.vue';
import Login from '../views/login.vue';
import Signup from '../views/signup.vue';
import adminlogin from '../views/adminlogin.vue';
import admindash from '../views/admindash.vue';
import subjectsview from '../views/subjectsview.vue';
import chapters from '../views/chapters.vue';
import addsub from '../views/addsub.vue';
import addchap from '../views/addchap.vue';
import viewchapter from '../views/viewchapter.vue';
import addquiz from '../views/addquiz.vue';
import viewquiz from '../views/viewquiz.vue';
import addquest from '../views/addquest.vue';
import editsub from '../views/editsub.vue';
import editchap from '../views/editchap.vue';
import editquiz from '../views/editquiz.vue';
import viewusers from '../views/viewusers.vue';
import stats from '../views/stats.vue';
import userdash from '../views/userdash.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        { path: '/', name: 'home', component: Hello },
        { path: '/login', name: 'login', component: Login },
        { path: '/signup', name: 'signup', component: Signup },
        { path: '/adminlogin', name: 'adminLogin', component: adminlogin },
        { path: '/admindash', name: 'admindash', component: admindash },
        { path: '/admindash/subjects', name: 'subjectview', component: subjectsview },
        { path: '/admindash/subject/:subject_id', name: 'chapters', component: chapters },
        { path: '/admindash/createsubject', name: 'addsub', component: addsub },
        { path: '/createchapter/:subject_id', name: 'addchap', component: addchap },
        { path: '/chapter/:chapter_id', name: 'viewchapter', component: viewchapter },
        { path: '/createquiz/:chapter_id', name: 'addquiz', component: addquiz },
        { path: '/quiz/:quiz_id', name: 'viewquiz', component: viewquiz },
        { path: '/createquestion/:quiz_id', name: 'addquest', component: addquest },
        { path: '/editsubject/:subject_id', name: 'editsub', component: editsub },
        { path: '/editchapter/:chapter_id', name: 'editchap', component: editchap },
        { path: '/editquiz/:quiz_id', name: 'editquiz', component: editquiz },
        { path: '/admindash/user', name: 'viewuser', component: viewusers },
        { path: '/admindash/stats', name: 'stats', component: stats },
        { path: '/userdash', name: 'userdash', component: userdash }
    ]
});

export default router;
