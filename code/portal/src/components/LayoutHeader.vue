<script setup>
import IconMail from '@/components/icons/IconMail.vue';
import IconArticle from '@/components/icons/IconArticle.vue';
import IconRoot from '@/components/icons/iconRoot.vue';
import { RouterLink, useRouter } from 'vue-router';
import { useScreenStore } from '@/stores/Screen';
const ScreenStore = useScreenStore();

ScreenStore.finishLoading();
</script>


<template>
  <div>
    <div>
      <RouterLink to="/" class="btn btn-ghost normal-case text-xl">
        <div class="flex flex-row justify-center m-3">
          <img class="mx-auto w-36" src="/logoCEDICA.png" alt="CEDICA" />
        </div>
      </RouterLink>
    </div>

    <nav class="flex justify-center mb-6">
      <div class="button-container">
        <RouterLink to="/" class="button">
          <div class="nav-item">
            <IconRoot class="icon" />
            <span class="tooltip">Inicio</span>
          </div>
        </RouterLink>
        <RouterLink to="/actividades_noticias" class="button">
          <div class="nav-item">
            <IconArticle class="icon" />
            <span class="tooltip">Artículos</span>
          </div>
        </RouterLink>
        <RouterLink to="/contacto" class="button">
          <div class="nav-item">
            <IconMail class="icon" />
            <span class="tooltip">Contacto</span>
          </div>
        </RouterLink>

      </div>
    </nav>
  </div>
</template>

<style scoped>
.button-container {
  display: flex;
  background-color: rgb(27, 133, 219);
  width: 250px;
  height: 40px;
  align-items: center;
  justify-content: space-around;
  border-radius: 10px;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px,
    rgba(27, 133, 219, 0.5) 5px 10px 15px;
}

.button {
  outline: 0 !important;
  border: 0 !important;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: all ease-in-out 0.3s;
  cursor: pointer;
}

.button:hover {
  transform: translateY(-3px);
}

.icon {
  font-size: 20px;
}


.nav-item {
  position: relative;
  margin: 0 15px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.nav-item:hover {
  transform: scale(1.1);
}

.nav-item .tooltip {
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  color: #000;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 12px;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.1);
  opacity: 0;
  pointer-events: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.nav-item .tooltip::before {
  content: "";
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 8px;
  height: 8px;
  background: #fff;
}

.nav-item:hover .tooltip {
  opacity: 1;
  top: -35px;
}
</style>
