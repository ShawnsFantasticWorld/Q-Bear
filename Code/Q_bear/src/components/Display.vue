<!--
Program Name: Questionnaire filling page
Function: The user opens the questionnaire link to fill in the questionnaire
-->
<template>
  <div class="display">
    <div class="content">
      <h3>{{title}}</h3>
      <div class="top" v-if="desc!=''">
        {{desc}}
      </div>
      <el-card class="box-card" v-for="(item,index) in detail">
        <div slot="header" class="clearfix">

          <div class="questionTitle">
            <!--Show required logo-->
            <span style="color: #F56C6C;">
              <span v-if="item.must">*</span>
              <span v-else>&nbsp;</span>
            </span>
            {{(index+1)+'.'+item.title}}
          </div>
        </div>

        <!--Single choice display-->
        <div class="text item" v-if="item.type=='radio'" v-for="optionItem in item.options">
          <el-radio v-model="item.radioValue" :label="optionItem.id" style="margin: 5px;">{{ optionItem.title }}</el-radio>
        </div>

        <!--Multiple choice display-->
        <el-checkbox-group v-if="item.type=='checkbox'" v-model="item.checkboxValue">
          <div class="text item"  v-for="optionItem in item.options">
            <el-checkbox :label="optionItem.id" style="margin: 5px;">{{ optionItem.title }}</el-checkbox>
          </div>
        </el-checkbox-group>

        <!--Fill in the blank display-->
        <el-input
          v-if="item.type=='text'"
          type="textarea"
          :rows="item.row"
          v-model="item.textValue"
          resize="none">
        </el-input>

      </el-card>
       <el-button type="primary" style="margin: 5px;" @click="submit" :loading="submitLoading">{{submitText}}</el-button>

      <div class="bottom">
        <el-link type="info" href="/index">Q-bear&nbsp;provide technical support</el-link>
      </div>
    </div>
  </div>
</template>
<script>
  import {answerOpera} from './api'
  export default{
    data(){
      return{
        dialogShow:false,
        dialogTitle:'',
        dialogType:1, // 1: Add 2: Edit
        oldItem:null, // Editing the object of the question
        willAddQuestion:{
          type:'',
          title:'',
          options:[''],
          text:'',
          row:1,
        },
        allType:[
          {
            value:'radio',
            label:'Single choice',
          },
          {
            value:'checkbox',
            label:'Multiple choice',
          },
          {
            value:'text',
            label:'Fill blank',
          },
        ],
        title:'',
        desc:'',
        detail:[],
        startTimestamp:0,// Questionnaire start timestamp milliseconds
        submitLoading:false,// Submit button loading state
        submitText:'Submit',// Submit button text
      }
    },
    mounted(){
      var wjId=this.$route.params.id;
      answerOpera({
        opera_type:'get_info',
        wjId:wjId,
        username:'test'// No need to pass after adding login verification (the backend gets it from the session)
      })
        .then(data=>{
          console.log(data);
          if(data.code==0){
            this.title=data.title;
            this.desc=data.desc;
            this.detail=data.detail;
            document.title=data.title;
          }
          else{
            this.$message({
              type: 'error',
              message: data.msg
            });
          }
        })
      this.startTimestamp=new Date().getTime();// Timestamp (ms) 
    },
    methods:{
      // Submit questionnaire
      submit(){
        this.submitLoading=true;
        this.submitText='Submitting';
        var wjId=this.$route.params.id;
        let useTime=parseInt((new Date().getTime()-this.startTimestamp)/1000);// Time to fill out the questionnaire (s)
        answerOpera({
          opera_type:'submit_wj',
          wjId:wjId,
          useTime:useTime,
          detail:this.detail
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              // Submitted successfully
              this.submitLoading=false;
              this.submitText='Submit';
              this.$router.push({path:'/thankyou'});// Jump to welcome page
            }
            else{
              this.submitLoading=false;
              this.submitText='Submit';
              this.$notify.error({
                title: 'Error',
                message: data.msg,
              });
            }
          })
      }
    }
  }
</script>
<style scoped>
  .display{
    text-align: center;
    padding: 20px;
  }
  .display .top{
    color: #606266;
    padding: 0 10px 10px 10px;
    border-bottom: 3px solid #409EFF;
    font-size: 15px;
    line-height: 22px;
    text-align: left;
  }
  .display .content{
    width: 100%;
    max-width: 800px;
    display: inline-block;
    text-align: center;
  }
  .display .box-card{
    text-align: left;
    width: 100%;
    margin:10px 0 10px 0;
  }
  .display .bottom{
    margin: 20px 10px 20px 10px;
    color: #909399;
  }
  .display a:link,a:visited,a:active {
    color: #909399;
    text-decoration:none;
  }
</style>
