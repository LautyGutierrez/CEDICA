import { defineStore } from 'pinia';

export const useScreenStore = defineStore('screen', {
  state: () => ({
    initializing: true,
    enabled: true,
  }),
  actions: {
   
    setLoading(value) {
      this.initializing = value;
    },
  
    finishLoading() {
        setTimeout(() => {
          this.setLoading(false); 
          this.enabled = false;
        }, 3000); 
      }
      
  }
});
