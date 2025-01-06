<template>
    <div>
        <div class="filters flex flex-col md:flex-row justify-center flex-wrap gap-4 p-4 bg-gray-200 rounded-md">
            <input v-model="filters.author" type="text" placeholder="Email del autor"
                class="input rounded-md p-2 border border-gray-300 w-full sm:w-3/4 md:w-1/4" />
            <div class="flex items-center gap-2 w-full sm:w-3/4 md:w-auto">
                <label for="published_from" class="self-center">Desde:</label>
                <input v-model="filters.published_from" type="date"
                    class="input rounded-md p-2 border border-gray-300 w-full md:w-auto" />
            </div>
            <div class="flex items-center gap-2 w-full sm:w-3/4 md:w-auto">
                <label for="published_to" class="self-center">Hasta:</label>
                <input v-model="filters.published_to" type="date"
                    class="input rounded-md p-2 border border-gray-300 w-full md:w-auto" />
            </div>
            <div class="flex gap-4 w-full justify-center md:justify-start md:w-auto">
                <button @click="applyFilters"
                    class="btn bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 w-full md:w-auto">
                    Buscar
                </button>
                <button @click="clearFilters"
                    class="btn bg-gray-400 text-white p-2 rounded-md hover:bg-gray-500 w-full md:w-auto">
                    Limpiar Filtros
                </button>
            </div>
        </div>

        <p v-if="loading">
            <LoaderNoticiasView></LoaderNoticiasView>
        </p>
        <div v-if="error" class="flex justify-center m-3">
            <p
                class="p-2 flex text-red-500 bg-red-100 rounded-2xl text-center w-1/2 text-pretty text-xl justify-center items-center">
                {{ error }}</p>
        </div>
        <div v-else class="flex justify-center mt-4" v-if="!loading && !actividad_noticia.length">
            <p
                class="p-10 flex bg-sky-700 rounded-2xl text-center w-1/2 text-white text-pretty text-xl justify-center items-center">
                <svg class="m-2" xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24">
                    <mask id="lineMdFileDocumentCancelTwotone0">
                        <g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                            <path fill="#fff" fill-opacity="0" stroke-dasharray="64" stroke-dashoffset="64"
                                d="M13.5 3l5.5 5.5v11.5c0 0.55 -0.45 1 -1 1h-12c-0.55 0 -1 -0.45 -1 -1v-16c0 -0.55 0.45 -1 1 -1Z">
                                <animate fill="freeze" attributeName="fill-opacity" begin="0.8s" dur="0.15s"
                                    values="0;0.3" />
                                <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.6s" values="64;0" />
                            </path>
                            <path d="M14.5 3.5l2.25 2.25l2.25 2.25z" opacity="0">
                                <animate fill="freeze" attributeName="d" begin="0.6s" dur="0.2s"
                                    values="M14.5 3.5l2.25 2.25l2.25 2.25z;M14.5 3.5l0 4.5l4.5 0z" />
                                <set fill="freeze" attributeName="opacity" begin="0.6s" to="1" />
                            </path>
                            <path stroke-dasharray="8" stroke-dashoffset="8" d="M9 13h6">
                                <animate fill="freeze" attributeName="stroke-dashoffset" begin="1s" dur="0.2s"
                                    values="8;0" />
                            </path>
                            <path stroke-dasharray="4" stroke-dashoffset="4" d="M9 17h3">
                                <animate fill="freeze" attributeName="stroke-dashoffset" begin="1.2s" dur="0.2s"
                                    values="4;0" />
                            </path>
                            <path fill="#000" fill-opacity="0" stroke="#000" stroke-dasharray="32"
                                stroke-dashoffset="32" stroke-width="6"
                                d="M18.5 14c2.48 0 4.5 2.02 4.5 4.5c0 2.48 -2.02 4.5 -4.5 4.5c-2.48 0 -4.5 -2.02 -4.5 -4.5c0 -2.48 2.02 -4.5 4.5 -4.5Z">
                                <set fill="freeze" attributeName="fill-opacity" begin="1.4s" to="1" />
                                <set fill="freeze" attributeName="stroke-dashoffset" begin="1.4s" to="0" />
                            </path>
                            <path stroke-dasharray="32" stroke-dashoffset="32"
                                d="M18.5 14c2.48 0 4.5 2.02 4.5 4.5c0 2.48 -2.02 4.5 -4.5 4.5c-2.48 0 -4.5 -2.02 -4.5 -4.5c0 -2.48 2.02 -4.5 4.5 -4.5Z">
                                <animate fill="freeze" attributeName="stroke-dashoffset" begin="1.4s" dur="0.4s"
                                    values="32;0" />
                            </path>
                            <path stroke-dasharray="10" stroke-dashoffset="10" d="M16 16l5 5">
                                <animate fill="freeze" attributeName="stroke-dashoffset" begin="1.8s" dur="0.2s"
                                    values="10;0" />
                            </path>
                        </g>
                    </mask>
                    <rect width="24" height="24" fill="white" mask="url(#lineMdFileDocumentCancelTwotone0)" />
                </svg>No se encuentran actividades ni noticias publicadas
            </p>
        </div>

        <div v-if="!loading && actividad_noticia.length"
            class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 p-4">
            <div class="card shadow-md rounded-lg overflow-hidden p-6 transition-all hover:shadow-xl"
                v-for="a_n in paginatedData" :key="a_n.id">
                <RouterLink class="btn" :to="{ name: 'actividad_noticia_detalle', params: { id: a_n.id } }">
                    <p class="card-title mb-2">{{ a_n.title }}</p>
                    <p class="small-desc mb-2">
                        {{ a_n.summary }}
                    </p>
                    <p class="small-desc">
                        Fecha publicación: <br>
                        {{ formatDate(a_n.date_publication) }}
                    </p>
                    <div class="go-corner">
                        <div class="go-arrow">
                            →
                        </div>

                    </div>
                </RouterLink>
            </div>
        </div>


        <div class="m-5">

            <Pagination v-if="!loading && actividad_noticia.length" :value="currentPage" :total="totalItems"
                :perPage="perPage" :loading="loading" :maxPage="totalPages" @update:value="onPageChange" />

        </div>

    </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useActividadNoticiaStore } from '../stores/actividadNoticia';
import { storeToRefs } from 'pinia';
import dayjs from 'dayjs';
import 'dayjs/locale/es';
import Pagination from '@/components/PaginationBar.vue';
import LoaderNoticiasView from '@/views/LoaderNoticiasView.vue';
import NotificactionToast from './NotificactionToast.vue';
dayjs.locale('es');
const formatDate = (dateString) => dayjs(dateString).format('D [de] MMMM [de] YYYY');
const store = useActividadNoticiaStore();
const { actividad_noticia, loading, totalItems, error } = storeToRefs(store);

const currentPage = ref(1);
const perPage = ref(9);


const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * perPage.value;
    const end = start + perPage.value;
    return actividad_noticia.value.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(totalItems.value / perPage.value);
});

const onPageChange = (newPage) => {
    if (newPage <= totalPages.value && newPage > 0) {
        currentPage.value = newPage;
    }
};


const filters = ref({
    author: '',
    published_from: '',
    published_to: '',
});

const applyFilters = async () => {
    if (filters.value.published_from && filters.value.published_to) {
        const fromDate = dayjs(filters.value.published_from);
        const toDate = dayjs(filters.value.published_to);

        if (fromDate.isAfter(toDate)) {
            error.value = "La fecha 'desde' no puede ser posterior a la fecha 'hasta'.";
            return;
        }
    }

    error.value = "";
    await store.fetchActividadNoticia({
        author: filters.value.author,
        published_from: filters.value.published_from,
        published_to: filters.value.published_to,
    });
};

onMounted(() => {
    store.fetchActividadNoticia();
});

const clearFilters = async () => {
    filters.value = {
        author: '',
        published_from: '',
        published_to: '',
    };
    error.value = "";
    await store.fetchActividadNoticia();
};

</script>


<style scoped>
.card-title {
    color: #262626;
    font-size: 1.5em;
    line-height: normal;
    font-weight: 700;
    margin-bottom: 0.5em;
}

.small-desc {
    font-size: 1em;
    font-weight: 400;
    line-height: 1.5em;
    color: #452c2c;
}

.small-desc {
    font-size: 1em;
}

.go-corner {
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    width: 2em;
    height: 2em;
    overflow: hidden;
    top: 0;
    right: 0;
    background: linear-gradient(135deg, #6293c8, #cbd44b);
    border-radius: 0 4px 0 32px;
}

.go-arrow {
    margin-top: -4px;
    margin-right: -4px;
    color: white;
    font-family: courier, sans;
}

.card {
    display: block;
    position: relative;
    background-color: #f2f8f9;
    border-radius: 20px;
    text-decoration: none;
    z-index: 0;
    overflow: hidden;
    background: linear-gradient(to bottom, #f0feff, #dee6ee);
    font-family: Arial, Helvetica, sans-serif;
}

.card:before {
    content: '';
    position: absolute;
    z-index: -1;
    top: -16px;
    right: -16px;
    background: linear-gradient(135deg, #6293c8, #cbd44b);
    height: 52px;
    width: 52px;
    border-radius: 32px;
    transform: scale(1);
    transform-origin: 50% 50%;
    transition: transform 0.35s ease-out;
}

.card:hover:before {
    transform: scale(28);
}

.card:hover .small-desc {
    transition: all 0.5s ease-out;
    color: rgba(255, 255, 255, 0.8);
}

.card:hover .card-title {
    transition: all 0.5s ease-out;
    color: #ffffff;
}
</style>