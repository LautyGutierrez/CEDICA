import { defineStore } from 'pinia'
import axios from 'axios'
import { BACKEND_BASE_URL } from '@/config'
export const useFormularioContactoStore = defineStore('formulario_contacto', {
    state: () => ({
        formulario: {
            nombre: '',
            apellido: '',
            email: '',
            cuerpo_mensaje: '',
        },
        loading: false,
        error: null,
    }),
    actions: {
        async enviarFormularioContacto({ recaptcha_token }) {
            try {
                this.loading = true
                this.error = null
                
                const payload = {
                    ...this.formulario,
                    recaptcha_token,
                };
                const response = await axios.post(`${BACKEND_BASE_URL}/contact/`, payload)
                this.resetFormulario()
            } catch {
                this.error = 'Error al obtener la información';
            } finally {
                this.loading = false;
            }
        },
        resetFormulario() {
            this.formulario = {
                nombre: '',
                apellido: '',
                email: '',
                cuerpo_mensaje: '',
            }
        }
    }
})