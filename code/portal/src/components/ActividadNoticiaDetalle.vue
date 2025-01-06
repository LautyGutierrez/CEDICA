<template>
    <div class="card bg-sepia-100 text-gray-800 w-auto h-auto rounded-lg shadow-md p-6 border border-gray-500">
        <ButtonBack></ButtonBack>
        <h1 class="text-3xl font-serif font-bold mb-2 border-b pb-2 border-gray-400">Título:</h1>
        <h1 class="text-4xl font-serif font-bold mb-4">{{ noticia.title }}</h1>
        <p class="text-lg font-serif font-bold mb-1 no-border">Resumen:</p>
        <p class="text-lg font-serif mb-3">{{ noticia.summary }}</p>
        <p class="text-lg font-serif font-bold mb-1 no-border">Contenido:</p>
        <p class="text-lg font-serif mb-3 break-words">{{ noticia.content_text }}</p>


        <p class="text-lg font-serif mb-3">
            <span class="font-bold">Autor:</span> {{ noticia.email }}
        </p>
        <p class="text-lg font-serif mb-3">
            <span class="font-bold">Fecha de Publicación:</span> {{ formatFecha(noticia.date_publication) }}
        </p>
        <p class="text-lg font-serif mb-3">
            <span class="font-bold">Fecha de Creación:</span> {{ formatFecha(noticia.date_creation) }}
        </p>
        <p class="text-lg font-serif mb-3">
            <span class="font-bold">Fecha de Actualización:</span>
            {{ noticia.date_update ? formatFecha(noticia.date_update) : 'No se actualizó el artículo aún' }}
        </p>
    </div>
</template>




<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useActividadNoticiaStore } from '../stores/actividadNoticia';
import ButtonBack from '@/components/ButtonBack.vue';

const route = useRoute();
const store = useActividadNoticiaStore();
const noticia = ref({});


const formatFecha = (fecha) => {
    if (!fecha) 
        return '';
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(fecha).toLocaleDateString('es-ES', options);
};

onMounted(() => {
    const id = parseInt(route.params.id);
    noticia.value = store.actividad_noticia.find((n) => n.id === id);
});
</script>


<style scoped>
.card {
    max-width: 800px;
    margin: 0 auto;
    background: #e9e9e4;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), inset 0 -2px 10px rgba(0, 0, 0, 0.05);
    border-radius: 10px;
    font-family: "Times New Roman", serif;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/old-wall.png');
    opacity: 0.1;
    z-index: -1;
}


.card h1 {
    text-transform: uppercase;
    letter-spacing: 1px;
}



.card p:not(.no-border) {
    border-bottom: 1px dashed #ccc;
    padding-bottom: 8px;
    margin-bottom: 12px;
}
</style>
