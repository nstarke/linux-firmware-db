<template>
  <h1>
        Linux Firmware DB
  </h1>
  <RouterView />
</template>

<script>
import { RouterView } from "vue-router";
export default {
  name: 'App',
  components: {
    RouterView
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
