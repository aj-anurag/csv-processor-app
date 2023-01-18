import {createRouter, createWebHistory} from 'vue-router'
import home from '../views/home.vue'
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: home
        },
        {
            path: '/files',
            component: () => import('../views/files.vue')
        }

    ]
})

export default router