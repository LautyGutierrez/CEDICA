<script setup>
  const props = defineProps({
    btnClass: {
      type: String,
      default: 'btn-primary'
    },
    disabled: {
      type: Boolean,
      default: false
    }
  });

  function goBack() {
    window.history.back();
  }
</script>

<template>
  <button :class="'flex mb-4 font-bold btn ' + props.btnClass" :disabled="props.disabled" @click="goBack">
    <slot> <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="black" d="M10.707 8.707a1 1 0 0 0-1.414-1.414l-4 4a1 1 0 0 0 0 1.414l4 4a1 1 0 0 0 1.414-1.414L8.414 13H18a1 1 0 1 0 0-2H8.414z"/></svg> Volver</slot>
  </button>
</template>