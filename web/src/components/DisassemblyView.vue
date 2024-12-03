<template>
    <div class="container">
        <p class="text-danger">
            {{  errorMsg }}
        </p>
        <p class="text-info">
            Disassembly assumes a naive base address of 0.  
        </p>
    </div>
    <div v-if="!noState">
          <span><b>File Name: </b>{{ state.file_name }} </span> |
          <span><b>SHA256: </b>{{ state.sha256 }} </span> |
          <span><b>Shannon Entropy: </b> {{ state.shannon_entropy }} </span> |
          <span><b>Full Arch: </b> {{ state.full_arch }} </span> |
          <span><b>Chunk Arch: </b> {{ state.chunk_arch }} </span> |
          <span><b>Full Length: </b> {{ state.full_length }} </span> |
          <span><b>Chunk Length: </b> {{ state.chunk_length }} </span> |
          <span><b>Chunk Count: </b> {{ state.chunk_count }} </span>
        </div>
    <textarea v-model="disassembly" class="form-control">
        </textarea>
  </template>
  
  <script>
  export default {
    name: 'DisassemblyView',
    data() {
        return {
            errorMsg: '',
            disassembly: '',
            noState: false,
            state: {}
        }
    },
   async mounted() {
      const data = localStorage.getItem('state');
      if (data) {
        this.noState = false;
        this.state = JSON.parse(data);
        if (this.$route.params.sha256 !== this.state.sha256) {
          localStorage.clear();
          this.state = { }
          this.noState = true;
        }
      } else {
        this.noState = true;
      }

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
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
  }
  a {
    color: #42b983;
  }
  textarea {
    resize: none;
    outline: none;
    width: 100%;
    border: none;
    height: 100vh;
  }
  </style>
  