<template>
    <div class="stuff">
        <p class="text-danger">
            {{  errorMsg }}
        </p>
        <p class="text-info">
            Disassembly assumes a naive base address of 0.  
        </p>
        <textarea v-model="disassembly" class="form-control">
        </textarea>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DisassemblyView',
    data() {
        return {
            errorMsg: '',
            disassembly: ''
        }
    },
   async mounted() {
      let res = await fetch('/data/txt/disassembly/linux-firmware-db-' + this.$route.params.sha256 + "-disassembly.txt")
      if (res.status === 200) {
        this.disassembly = await res.text()
      } else {
        this.errorMsg = "Disassembly not found, please try again later"
      }
    },
    computed: {
    },
    methods: {
    }
  }
  
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  div, textarea {
  resize: none;
  outline: none;
  width: 100%;
  padding: 10px;
  border: none;
  height: 100vh;
  margin: -10px;
}
  </style>
  