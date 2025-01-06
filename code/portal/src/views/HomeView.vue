<script setup>
import InfoButton from '@/components/InfoButton.vue';


</script>

<template>
  <div class="h-full overflow-y-auto">
    <main class="mx-auto p-4">
      <section class="flex flex-col justify-center items-center gap-8 mb-12">
        <div class="container mx-auto bg-blue-400/70 p-8 rounded-md">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="flex flex-col">
              <h1 class="text-4xl md:text-5xl leading-normal font-bold text-left text-neutral-900">
                CEDICA
              </h1>
              <h2 class="text-2xl font-bold text-left md:text-3xl text-neutral-900 p-1">
                ¿Quiénes somos?
              </h2>
              <p class="text-gray-800 text-lg">
                El Centro de Equitación para Personas con Discapacidad y Carenciadas, CEDICA, es una Asociación Civil
                sin
                Fines de Lucro, fundada en 1994 en la ciudad de La Plata, Provincia de Buenos Aires.

                La misión de CEDICA es la INCLUSIÓN SOCIAL: trabajamos con la finalidad de igualar oportunidades en
                procura de
                la reinserción familiar, el logro de la escolaridad, la integración laboral y la mejora integral de la
                calidad
                de vida de nuestros alumnos y alumnas.

                La actividad que realizamos se denomina internacionalmente Rehabilitación Ecuestre y es una terapia
                integral
                que apunta a la recuperación de la persona en sus dimensiones biológica, psíquica y social.
              </p>
              <img src="/Cedica-1.jpg" alt="Imagen 1 de Cedica"
                class="w-full h-auto rounded-md mb-4 transition-transform duration-300 ease-in-out hover:scale-105 mt-4">
              <p class="text-gray-800 text-lg">
                La Rehabilitación Ecuestre utiliza al caballo de manera terapéutica, aprovechando las características de
                su
                naturaleza innata y de su medio ambiente como facilitadores del proceso rehabilitador.

                Los alumnos y alumnas del CEDICA son personas con distintos niveles de discapacidad física y/o mental,
                que
                pueden presentar patologías asociadas, así como individuos en situaciones de riesgo y vulnerabilidad
                social.
                Provienen de Institutos de Menores, Hospitales y Centros de Salud, otras ONG’s, barrios carenciados y/o
                familias vulnerables.

                Las actividades son totalmente gratuitas para todos los alumnos y alumnas, que son becados gracias a los
                aportes del Ministerio de Desarrollo Social, el Instituto de Loterías y Casinos de la Provincia de
                Buenos
                Aires, el Hipódromo de La Plata y el Campo Arroyo San Juan.

                En el Programa de Voluntariado de CEDICA, las personas que desean sumarse a la institución reciben una
                capacitación durante la cual adquieren el conocimiento necesario para desempeñarse como Operadores de
                Pista.
              </p>
            </div>
            <div class="flex flex-col">
              <img src="/Cedica-2.jpg" alt="Imagen 2 de Cedica"
                class="w-full h-auto rounded-md mb-4 transition-transform duration-300 ease-in-out hover:scale-105 mt-4">
              <p class="text-gray-800 text-lg">
                Los Voluntarios firman un Compromiso de Honor mediante el cual se comprometen a trabajar una tarde por
                semana
                durante un año, complementando la tarea del Equipo de CEDICA.

                CEDICA funciona desde su fundación en instalaciones cedidas por el Hipódromo de La Plata, en donde
                contamos no
                sólo con una Nueva Pista de Actividades Ecuestres, Oficina y Salón de Capacitación, sino también con el
                alojamiento de nuestros caballos, también gracias a la generosidad de la Escuela de Jockeys.

                Además, desde 2008 sumamos una segunda sede: el campo Arroyo San Juan en la localidad de Arturo Seguí,
                que
                nos
                ha permitido ampliar nuestra capacidad de atención y realizar actividades diferenciales gracias a la
                disponibilidad de algunas hectáreas abiertas de campo e instalaciones como picadero y tanque
                australiano.
              </p>
              <img src="/Cedica-3.jpg" alt="Imagen 3 de Cedica" class="w-full h-auto rounded-md mt-4 mb-4 transition-transform duration-300 ease-in-out hover:scale-105">
            </div>
          </div>
        </div>
      </section>

      <section class="p-6 flex flex-col items-center my-12">
        <h2 class="text-2xl font-bold text-center md:text-3xl text-neutral-900">
          ¡Contactanos!
        </h2>
        <address class="mt-4 xs:mt-8 text-lg leading-relaxed">
          <ul>
            <li>Dirección: Calle 44 y 115, La Plata </li>
            <li>Teléfono: +54 9 221 506-6291</li>
            <li>Email:
              <a href="mailto: equitacionparatodos@gmail.com" class="hover:underline hover:text-blue-500">
                equitacionparatodos@gmail.com
              </a>
            </li>
          </ul>
        </address>
        <InfoButton></InfoButton>
      </section>
    </main>
  </div>


</template>