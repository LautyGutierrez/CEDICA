<script setup>
  import LayoutHeader from '@/components/LayoutHeader.vue';
  import ToastNotifications from '@/components/NotificactionToast.vue';
  import { useScreenStore } from '@/stores/Screen';
  import Screen from '@/views/Screen.vue';
  import { RouterView } from 'vue-router';

  const ScreenStore = useScreenStore();

 
  ScreenStore.finishLoading();
</script>

<template>
  <ToastNotifications />

 
  <Screen v-if="ScreenStore.enabled" :is-loading="ScreenStore.initializing" />

  <header class="flex-none">
    <LayoutHeader />
  </header>

  <div class="flex-1 ">
    <RouterView />
  </div>
</template>
