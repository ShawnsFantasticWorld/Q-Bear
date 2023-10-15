<template>
  <div>
    <el-radio v-model="radio" label="1">Alternative</el-radio>
    <el-radio v-model="radio" label="2">Alternative</el-radio>

    {{radio}}

    <el-button type="primary" @click="test">Main button</el-button>
  </div>
</template>
<script>
  export default{
    data(){
      return{
        radio:'1'
      }
    },
    methods:{
      test(){
        console.log(this.radio);
      }
    },
    mounted(){

    },
    computed:{

    },
  }
</script>
<style>

</style>
