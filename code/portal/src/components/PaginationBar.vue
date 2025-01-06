<script setup>
  import IconLoader from '@/components/icons/IconLoader.vue';
  import { ref, computed, onMounted } from 'vue';

  const props = defineProps({
    value: {
      type: Number,
      default: 1
    },
    total: {
      type: Number,
      default: 0
    },
    perPage: {
      type: Number,
      default: 10
    },
    loading: {
      type: Boolean,
      default: false
    }
  });

  defineEmits(['update:value']);

  const MAXIMUN_PAGES = 10;

  const last = computed(() => Math.ceil(props.total / props.perPage));
  const pages = computed(() => {
    const pages = [];
    const totalPages = Math.ceil(props.total / props.perPage);
    const start = Math.max(1, props.value - Math.floor(MAXIMUN_PAGES / 2));
    const end = Math.min(totalPages, start + MAXIMUN_PAGES - 1);
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  });

  const canGoToPrevious = computed(() => props.value > 1);
  const canGoToNext = computed(() => props.value < last.value);
</script>

<template>
  <div class="flex justify-center flex-wrap gap-2">
    
    <template v-if="canGoToPrevious">
      <button class="font-bold" @click="$emit('update:value', props.value - 1)" title="Anterior">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="black" d="M13.54 18a2.06 2.06 0 0 1-1.3-.46l-5.1-4.21a1.7 1.7 0 0 1 0-2.66l5.1-4.21a2.1 2.1 0 0 1 2.21-.26a1.76 1.76 0 0 1 1.05 1.59v8.42a1.76 1.76 0 0 1-1.05 1.59a2.2 2.2 0 0 1-.91.2"/></svg>
      </button>
    </template>

    <template v-for="page in pages" :key="page">
      <button
        v-if="page === props.value"
        class="btn bg-blue-500 text-white text-lg px-4 py-2 rounded-md font-semibold transform scale-110 relative"
      >
        <IconLoader class="animate-spin absolute" :class="{ hidden: !props.loading }" />
        <span :class="{ 'text-transparent': props.loading }">{{ page }}</span>
      </button>
      <button 
        v-else 
        class="btn btn-primary text-lg px-4 py-2 rounded-md"
        @click="$emit('update:value', page)"
      >
        {{ page }}
      </button>
    </template>

    <template v-if="canGoToNext">
      <button
        class="font-bold"
        @click="$emit('update:value', props.value + 1)" 
        :title="last.toString()">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="black" d="M10.46 18a2.2 2.2 0 0 1-.91-.2a1.76 1.76 0 0 1-1.05-1.59V7.79A1.76 1.76 0 0 1 9.55 6.2a2.1 2.1 0 0 1 2.21.26l5.1 4.21a1.7 1.7 0 0 1 0 2.66l-5.1 4.21a2.06 2.06 0 0 1-1.3.46"/></svg>
      </button>
    </template>
  </div>
</template>
