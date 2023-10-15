<template>
  <div class="home">

    <!--Left navigation bar-->
    <el-menu
      :default-active="defaultActive"
      class="menu">

      <el-menu-item v-for="(item,index) in wjList" :index="(index+1).toString()">
        <i class="el-icon-tickets"></i>

        <span slot="title">{{item.title}}</span>

      </el-menu-item>

      <el-menu-item @click="dialogShow=true">
        <i class="el-icon-plus"></i>
        <span slot="title">Add quuestionnaire</span>
      </el-menu-item>
    </el-menu>



    <!--Add questionnaire popup-->
    <el-dialog title="Add questionnaire" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddWj" label-width="80px">
        <el-form-item label="Title" style="width: 100%;">
          <el-input v-model="willAddWj.title" placeholder="Please enter a title" ></el-input>
        </el-form-item>
      </el-form>
      <div style="width: 100%;text-align: right">
        <el-button type="primary" style="margin-left: 10px;" @click="addWj">Confirm</el-button>
      </div>
    </el-dialog>


    <!--Content area-->
    <div class="content">
      <design ref="design"></design>
    </div>

    <!--Right side operation bar-->
    <div class="right">
      <el-button type="success"  icon="el-icon-upload" style="margin: 5px;">Publish questionnaire</el-button><br>
      <el-button type="primary"  icon="el-icon-view" style="margin: 5px;">Preview questionnaire</el-button><br>
      <el-button type="danger"  icon="el-icon-delete" style="margin: 5px;">Delete questionnaire</el-button>

      <div>
        Status: Unpublished<br>
        Submition: 3<br>
        Browse: 28<br>
      </div>

    </div>
  </div>
</template>
<script>
  import Design from './Design.vue'
  export default{
    components:{
      Design,
    },
    data(){
      return{
        defaultActive:'1',// Currently active menu
        wjList:[
          {
            title:'Requirements Analysis and Survey on Questionnaire System',
            flag:0,// 0: Unreleased 1: Released
          },
        ],
        dialogShow:false,
        willAddWj:{
          title:'',
          flag:0
        }
      }
    },
    methods:{
      addWj(){
        this.wjList.push(this.willAddWj);
//        this.$refs.design.detail=[];
        this.dialogShow=false;
      }
    }
  }
</script>
<style scoped>
  .home{
    position: absolute;
    width: 100%;
    height: calc(100vh - 100px);
    text-align: left;

  }
  .home .badgeItem{
    margin-top: 40px;
  }
  .content{
    /*background-color: yellow;*/
    /*float: left;*/
    padding: 20px;
    width: 60%;
    height: 100%;
    text-align: center;
    display: inline-block;
    position: absolute;
    left: 20%;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .menu{
    /*float: left;*/
    width: 20%;
    background-color: white;
    height: calc(100vh - 60px);
    position: absolute;
    left: 0;
  }

  .home .right{
    background-color: yellow;
    position: absolute;
    left: 80%;
    margin-left: 40px;
    top:0;
    padding-top: 30px;
    padding-left: 30px;
  }
</style>
