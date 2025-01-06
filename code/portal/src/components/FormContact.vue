<style scoped>
  .form {
    --background: #f3f3f3;
    --input-focus: #2d8cf0;
    --font-color: #323232;
    --font-color-sub: #666;
    --bg-color: #fff;
    --main-color: #323232;
    padding: 20px;
    background: var(--background);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: 20px;
    border-radius: 5px;
    border: 2px solid var(--main-color);
    box-shadow: 4px 4px var(--main-color);
  }

  .form > p {
    font-family: var(--font-DelaGothicOne);
    color: var(--font-color);
    font-weight: 700;
    font-size: 20px;
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
  }

  .form > p > span {
    font-family: var(--font-SpaceMono);
    color: var(--font-color-sub);
    font-weight: 600;
    font-size: 17px;
  }

  .oauthButton {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    padding: auto 15px 15px auto;
    width: 400px;
    height: 40px;
    border-radius: 5px;
    border: 2px solid var(--main-color);
    background-color: var(--bg-color);
    box-shadow: 4px 4px var(--main-color);
    font-size: 16px;
    font-weight: 600;
    color: var(--font-color);
    cursor: pointer;
    transition: all 250ms;
    position: relative;
    overflow: hidden;
    z-index: 1;
  }

  .oauthButton::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0;
    background-color: #212121;
    z-index: -1;
    -webkit-box-shadow: 4px 8px 19px -3px rgba(0, 0, 0, 0.27);
    box-shadow: 4px 8px 19px -3px rgba(0, 0, 0, 0.27);
    transition: all 250ms;
  }

  .oauthButton:hover {
    color: #e8e8e8;
  }

  .oauthButton:hover::before {
    width: 100%;
  }

  .form > input {
    width: 400px;
    height: 40px;
    border-radius: 5px;
    border: 2px solid var(--main-color);
    background-color: var(--bg-color);
    box-shadow: 4px 4px var(--main-color);
    font-size: 15px;
    font-weight: 600;
    color: var(--font-color);
    padding: 5px 10px;
    outline: none;
  }

  .form > textarea {
    width: 400px;
    height: 150px; 
    border-radius: 5px;
    border: 2px solid var(--main-color);
    background-color: var(--bg-color);
    box-shadow: 4px 4px var(--main-color);
    font-size: 15px;
    font-weight: 600;
    color: var(--font-color);
    padding: 5px 10px;
    outline: none;
  }

  .icon {
    width: 1.5rem;
    height: 1.5rem;
  }
 
  .form-container {
    display: flex;
    flex-direction: column;
    justify-content: center; 
    align-items: center;   
;          
       
  }
</style>

<script setup>
  import { useFormularioContactoStore } from '../stores/formularioContacto';
    import { storeToRefs } from 'pinia';
    import { ref } from 'vue';
    import { useReCaptcha } from 'vue-recaptcha-v3';

    const errors = ref({
        nombre: '',
        apellido: '',
        email: '',
    });

    const validarNombreApellido = (valor) => /^[a-zA-ZÀ-ÿ\s']+$/.test(valor);
    const validarEmail = (valor) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(valor);

    const validarFormulario = () => {

        if ((!formulario.value.nombre) || (!formulario.value.apellido) || (!formulario.value.email)) {
            alert('Todos los campos son obligatorios.');
            return false;
        }

        if (!validarNombreApellido(formulario.value.nombre)) {
            errors.value.nombre = 'El nombre solo puede contener letras.';
            return false;
        }
        errors.value.nombre = '';

        if (!validarNombreApellido(formulario.value.apellido)) {
            errors.value.apellido = 'El apellido solo puede contener letras.';
            return false;
        } 
        errors.value.apellido = '';

        if (!validarEmail(formulario.value.email)) {
            errors.value.email = 'El email no tiene un formato válido.';
            return false;
        }
        errors.value.email = '';

        return true;
    };
    const { executeRecaptcha, recaptchaLoaded } = useReCaptcha();
    const captcha = async () => {
        await recaptchaLoaded()
        const token = await executeRecaptcha('submit_form')
        return token
    }
    const store = useFormularioContactoStore();
    const { formulario, loading, error } = storeToRefs(store);
    const submitForm = async () => {
        if (validarFormulario()) {
            try{
                const recaptcha_token = await captcha();
                await store.enviarFormularioContacto({...formulario, recaptcha_token});
                alert('Formulario enviado con éxito.');
                window.location.reload();
            } catch (error) {
                alert('Error al enviar el formulario.');
            }
        } else {
            if (errors.value.nombre || errors.value.apellido || errors.value.email)
              alert(errors.value.nombre || errors.value.apellido || errors.value.email);
        }
    };
</script>

<template>
  <div class="form-container">
    <form @submit.prevent="submitForm" class="form">
      <p>
        Contacto<span>Completá los siguientes campos para contactarnos</span>
      </p>
      <input type="text" id="nombre" v-model="formulario.nombre" placeholder="Nombre" name="nombre">
      <input type="text"  id="apellido" v-model="formulario.apellido"  placeholder="Apellido" name="apellido">
      <input type="email"  id="email" v-model="formulario.email" placeholder="Email" name="email">
      <textarea name="textarea" id="cuerpo_mensaje" v-model="formulario.cuerpo_mensaje" placeholder="Escribe tu mensaje aquí" required></textarea>
      <button type="submit" class="oauthButton">
        Contactar
        <svg class="icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m6 17 5-5-5-5"></path>
          <path d="m13 17 5-5-5-5"></path>
        </svg>
      </button>
    </form>
  </div>
</template>
