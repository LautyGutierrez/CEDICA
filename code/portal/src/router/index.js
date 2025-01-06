import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import FormContact from '@/components/FormContact.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not_found',
      component: NotFoundView
    },
    {
      path:'/actividades_noticias',
      name:'actividades_noticias',
      component: () => import('../views/ActividadesNoticiasView.vue'),
    },
    {
      path: '/completa/:id',
      name: 'actividad_noticia_detalle',
      component: () => import('../views/detalleNoticia.vue'),
      props: true,
    },
    {
      path: '/contacto',
      name: 'contacto',
      component: FormContact,
    }
  ],
})

export default router
