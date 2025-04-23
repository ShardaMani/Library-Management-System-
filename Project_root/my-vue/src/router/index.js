import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../components/HomePage.vue';
import UserLogin from '../components/UserLogin.vue';
import UserRegister from '../components/UserRegister.vue';
import LibrarianDashboard from '../components/LibrarianDashboard.vue';
import UserDashboard from '../components/UserDashboard.vue';
import Logout from '../components/Logout.vue';
import Sections from '../components/Section.vue'; // Import the Sections component
import UserProfile from '@/components/UserProfile.vue';
import Request from '@/components/Request.vue';
import MyBooks from '@/components/MyBooks.vue';
import Content from '@/components/Content.vue';
Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/login', name: 'Login', component: UserLogin },
    { path: '/register', name: 'Register', component: UserRegister },
    { path: '/librarian_dashboard', name: 'LibrarianDashboard', component: LibrarianDashboard },
    { path: '/user_dashboard', name: 'UserDashboard', component: UserDashboard },
    { path: '/sections', name: 'Sections', component: Sections }, // Add this route
    { path: '/logout', name: 'Logout', component: Logout },
    { path: '/profile', name: 'UserProfile', component: UserProfile},
    { path: '/MyBooks', name: 'MyBooks', component: MyBooks},
    { path: '/requests', name: 'Request', component: Request},
    { path: '/ebooks/:ebookId/content', name: 'Content', component: Content},
  ],

});
