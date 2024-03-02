<template>
  <div class="container-fluid">
    <div class="container">
      <p class="text-danger">
          {{  errorMsg }}
        </p>
        <p class="text-info">
          Linux Firmware DB is a data set of Instruction Set Architectures for each of the files in the <code>linux-firmware</code> git repository.
          <br />
          The goal of this project is to spread knowledge and awareness on the proprietary firmware blobs bundled with Linux.
          <br />
          The data set was built with <a href="https://github.com/airbus-seclab/cpu_rec">cpu_rec</a> and <a href="https://rada.re/n/">radare2</a>
          <br />
          See the repository for this project on <a href="https://github.com/nstarke/linux-firmware-db/">Github</a>
        </p>
    </div>
    <div class="container">
      <span>
        <div>
          Select Tag <select v-on:change="selectTagChanged" v-model="selectedTag" class="form-control">
              <option value="" disabled selected>
                  Choose Git Tag
              </option>
              <option v-for="tag in tags" :key="tag">
                {{ tag }}
              </option>
          </select>
        </div>
        <div v-if="selectedTag" class="form-group">
          <p>Filter</p>
          <div class="checkbox">
            <label>
              <input type="radio" :checked="dataOnly" v-model="dataOnly" v-on:click="dataOnlyClicked"> 
              Show only files with <code>data</code> file types (most likely to be firmware images)
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="radio" :checked="fullOnly" v-model="fullOnly" v-on:click="fullOnlyClicked"> 
              Show only files with an architecture detected for the entire file
            </label>
          </div>
          <div class="checkbox">
            <label>
              <input type="radio" :checked="noAscii" v-model="noAscii" v-on:click="noAsciiClicked"> 
              Don't Show Text Files
            </label>
          </div>
          <div class="input">
            <label>
              <input min="0" type="number" v-model="minimumFullSize" v-on:change="minimumFullSizeChanged">
              Minimum Full File Length
            </label>
          </div>
          <div class="input">
            <label>
              <input min="0" type="number" v-model="maximumFullSize" v-on:change="maximumFullSizeChanged">
              Maximum Full File Length
            </label>
          </div>
          <div class="input">
            Select Full Architecture <select v-on:change="fullArchTypeChanged" v-model="selectedFullArchType" class="form-control">
              <option value="" selected>
                All Arch
              </option>
              <option v-for="fullArchType in fullArchTypes" :key="fullArchType">
                {{ fullArchType }}
              </option>
            </select>
          </div>
        </div>
      </span>
      <span v-if="selectedTag" class="border">
        <span v-if="resultsCount > 0" class="text-primary">Results Count: {{ resultsCount }}</span>
        <span v-if="resultsCount === 0" class="text-warning">No Results</span>
      </span>
    </div>
    <div class="container">
      <table class="table table-striped table-bordered">
        <thead>
          <th class="text-center" v-on:click="performSort('file_name')">
            File Name
          </th>
          <th class="text-center" v-on:click="performSort('full_arch')">
            Full Arch
          </th>
          <th class="text-center" v-on:click="performSort('chunk_arch')">
            Chunk Arch
          </th>
          <th class="text-center" v-on:click="performSort('full_length')">
            Full Length
          </th>
          <th class="text-center" v-on:click="performSort('chunk_length')">
            Chunk Length
          </th>
          <th class="text-center" v-on:click="performSort('chunk_count')">
            Chunk Count
          </th>
          <th class="text-center" v-on:click="performSort('file_type')">
            File Type
          </th>
          <th class="text-center" v-on:click="performSort('shannon_entropy')">
            Shannon Entropy
          </th>
          <th class="text-center">
            Disassembly
          </th>
        </thead>
        <tbody>
          <tr v-for="result in results" :key="result.file_name">
            <td class="text-center"><a v-bind:href="`https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/tree/${result.file_name.substring(result.file_name.indexOf('/') + 1, result.file_name.length)}?h=${this.selectedTag}`">{{ result.file_name }}</a></td>
            <td class="text-center">{{ result.full_arch }}</td>
            <td class="text-center">{{ result.chunk_arch }}</td>
            <td class="text-center">{{ result.full_length }}</td>
            <td class="text-center">{{ result.chunk_length }}</td>
            <td class="text-center">{{ result.chunk_count }}</td>
            <td class="text-center">{{ result.file_type }}</td>
            <td class="text-center">{{ result.shannon_entropy }}</td>
            <td class="text-center" v-if="['SuperH', 'ARM', 'MIPS', 'X86', '8051', 'ARcompact', '6502'].some(term => result.full_arch.includes(term)) || ['ARM', 'MIPS', 'mips', '8051', '6502'].some(term => result.chunk_arch.includes(term)) ">
              <router-link v-on:click="disassemblyClicked(result)" :to="{ name: 'disassembly', params: { firmware: result, sha256: result.sha256 } }">View</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainView',
  data() {
    return {
      selectedFullArchType: localStorage.getItem('selectedFullArchType'),
      fullOnly: localStorage.getItem([this.selectedTag, 'fullOnly'].join('')) === 'true',
      dataOnly: localStorage.getItem([this.selectedTag, 'dataOnly'].join('')) === 'true',
      noAscii: localStorage.getItem([this.selectedTag, 'noAscii'].join('')) === 'true',
      selectedTag: localStorage.getItem('selectedTag'),
      errorMsg: '',
      tags: [],
      asc: true,
      results: [],
      json: [],
      minimumFullSize: parseInt(localStorage.getItem([this.selectedTag, 'minimumFullSize'].join())) || 0,
      maximumFullSize: 256 * 1024 * 1024,
      maximumPossibleSize: 0
    }
 },
 async mounted() {
    let res = await fetch('/data/json/tags.json')
    if (res.status === 200) {
      let json = await res.json()
      this.tags = json;
    } else {
      this.errorMsg = "Tags not found, please try again later"
    }
    this.getCache();
    this.json = JSON.parse(localStorage.getItem([this.selectedTag, 'data'].join('.'))) || [];
    this.results = this.json;
    this.performFilter();
  },
  computed: {
    resultsCount() {
      return this.results.length;
    },
    fullArchTypes() {
      return [...new Set(this.results.map((res)=> res.full_arch))].sort();
    }
  },
  methods: {
    disassemblyClicked(result) {
      localStorage.setItem('state', JSON.stringify(result));
    },
    async selectTagChanged() {
      this.results = [];
      localStorage.setItem('selectedTag', this.selectedTag);
      const data = localStorage.getItem([this.selectedTag, 'data'].join('.'));
      if (data) {
        this.json = JSON.parse(data);
        this.results = this.json;
      } else {
        let res = await fetch('/data/json/linux-firmware-db-' + this.selectedTag + '-cpu_rec.json');
        if (res.status === 200){
          this.json = await res.json();
          localStorage.setItem([this.selectedTag, 'data'].join('.'), JSON.stringify(this.json));
          this.results = this.json;
        } else {
          return this.errorMsg = res.statusText;
        }
      }

      this.performFilter();
    },
    dataOnlyClicked() {
      this.dataOnly = !this.dataOnly;
      localStorage.setItem('dataOnly', this.dataOnly);
      this.performFilter();
    },
    fullOnlyClicked() {
      this.fullOnly = !this.fullOnly;
      localStorage.setItem('fullOnly', this.fullOnly);
      this.performFilter();
    },
    noAsciiClicked() {
      this.noAscii = !this.noAscii;
      localStorage.setItem('noAscii', this.noAscii);
      this.performFilter();
    },
    minimumFullSizeChanged() {
      localStorage.setItem('minimumFullSize', this.minimumFullSize);
      this.performFilter();
    },
    maximumFullSizeChanged() {
      this.performFilter();
    },
    fullArchTypeChanged() {
      localStorage.setItem('selectedFullArchType', this.selectedFullArchType);
     
      this.performFilter();
    },
    performFilter() {
      if (this.dataOnly && this.fullOnly) {
        this.results = this.json.filter((res)=>{ return res.file_type === "data" && res.full_arch !== "None"});
      } else if (this.dataOnly && !this.fullOnly) {
        this.results = this.json.filter((res)=>{ return res.file_type === "data" });
      } else if (!this.dataOnly && this.fullOnly) {
        this.results = this.json.filter((res)=>{ return res.full_arch !== "None"});
      } else if (this.noAscii) {
        this.results = this.json.filter(res => res.file_type && !['ascii', 'unicode', 'utf-8', 'text'].some(i=>res.file_type.includes(i)));
      } else {
        this.results = this.json;
      }

      this.results = this.results.filter((res)=>{ return this.maximumFullSize >= res.full_length && this.minimumFullSize <= res.full_length; });
      if (this.selectedFullArchType) {
        this.results = this.results.filter((res)=>{ return res.full_arch === this.selectedFullArchType; });
      }

      if (this.results.length){
        this.maximumPossibleSize = this.results.reduce((prev, current) => (prev
          && Number.isInteger(current.full_length)
          && Number.isInteger(prev.full_length)
          && prev.full_length > current.full_length) ? prev : current);
        this.maximumFullSize = this.maximumPossibleSize.full_length;
      }
      this.getCache();
    },
    performSort(field) {
      this.asc = !this.asc;
      this.results.sort((a, b) => {
        if (a[field] > b[field] ) {
          return this.asc ? -1 : 1;
        } else if (a[field] < b[field] ) 
          return this.asc ? 1 : -1;
      });
    },
    getCache() {
      this.dataOnly = localStorage.getItem('dataOnly') === 'true';
      this.fullOnly = localStorage.getItem('fullOnly') === 'true';
      this.noAscii = localStorage.getItem('noAscii') === 'true';
      this.minimumFullSize = parseInt(localStorage.getItem('minimumFullSize')) || 0;
      this.selectedFullArchType = localStorage.getItem('selectedFullArchType');
    }
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
</style>
