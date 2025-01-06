
import { defineStore } from 'pinia'
import axios from 'axios'
import { BACKEND_BASE_URL } from '@/config'

export const useActividadNoticiaStore = defineStore('actividad_noticia', {
    state: () => ({
        actividad_noticia: [],
        loading: false,
        totalItems: 0,
        error: null,
    }),
    actions: {
        async fetchActividadNoticia({ author = '', published_from = '', published_to = '' } = {}) {
            try {
                this.loading = true;
                this.error = null;
             
                
                const params = {};
                if (author) params.author = author;
                if (published_from) params.published_from = published_from;
                if (published_to) params.published_to = published_to;
                const response = await axios.get(`${BACKEND_BASE_URL}/articles`, { params });
                this.actividad_noticia = response.data[0];
                this.totalItems = response.data[1].total;
             
            } catch {
                this.error = 'Error al obtener la información';
            } finally {
                this.loading = false;
            }
        },
    },
});
