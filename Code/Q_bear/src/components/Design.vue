<!--
Program Name: Question design page
Function: Adding, editing, and deleting questions in the questionnaire
-->
<template>
  <div class="Design" v-loading="loading" element-loading-text="Loading...">
    <h3>{{title}}</h3>
      <div class="top" v-if="desc!=''">
        {{desc}}
      </div>
    <el-card class="box-card" v-for="(item,index) in detail" style="margin: 10px;">
        <div slot="header" class="clearfix">
          <div class="questionTitle">
            <!--Show required logo-->
            <span style="color: #F56C6C;">
              <span v-if="item.must">*</span>
              <span v-else>&nbsp;</span>
            </span>
            <span style="color: black;margin-right: 3px;">{{(index+1)+'.'}}</span>
            {{item.title}}
          </div>
          <div style="float: right;">
            <el-button style="padding: 2px" type="text" @click="editorQuestion(item)">Edit</el-button>
            <el-button style="padding: 2px;color: #F56C6C" type="text" @click="deleteQuestion(index)">Delete</el-button>
          </div>
        </div>

        <!--Single choice display-->
        <div class="text item" v-if="item.type=='radio'" v-for="(option,index) in item.options">
          <el-radio v-model="item.radioValue" :label="index" style="margin: 5px;">{{ option.title }}</el-radio>
        </div>

        <!--Multiple choice display-->
        <el-checkbox-group v-if="item.type=='checkbox'" v-model="item.checkboxValue">
          <div class="text item"  v-for="(option,index) in item.options">
            <el-checkbox :label="index" style="margin: 5px;">{{ option.title }}</el-checkbox>
          </div>
        </el-checkbox-group>

        <!--Fill in the blank display-->
        <el-input
          v-if="item.type=='text'"
          type="textarea"
          :rows="item.row"
          resize="none"
          v-model="item.textValue">
        </el-input>

      </el-card>

      <el-button  icon="el-icon-circle-plus" @click="addQuestion" style="margin-top: 10px;">Add Question</el-button>

<br><br><br><br><br>

    <!--Add topic popup-->
    <el-dialog :title="dialogTitle" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddQuestion" label-width="80px">
        <el-form-item label="Question type" style="width: 100%;">
          <el-select v-model="willAddQuestion.type" placeholder="Please select a question type" @change="typeChange">
          <el-option
            v-for="item in allType"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        </el-form-item>
        <el-form-item label="Is it required?" style="width: 100%;">
          <el-checkbox v-model="willAddQuestion.must">Required</el-checkbox>
        </el-form-item>
        <el-form-item label="Title" style="width: 100%;">
          <el-input v-model="willAddQuestion.title" placeholder="Please enter a title" ></el-input>
        </el-form-item>

        <template v-if="willAddQuestion.type=='radio'||willAddQuestion.type=='checkbox'">
          <el-form-item :label="'Option'+(index+1)" v-for="(item,index) in willAddQuestion.options" >
            <el-row>
              <el-col :span="16">
                <el-input  v-model="item.title" placeholder="Please enter an option name" style="width: 90%;"></el-input>
              </el-col>
            <el-col :span="8">
              <el-button type="danger" plain class="" @click="deleteOption(index)" >Delete option</el-button>
            </el-col>
            </el-row>

          </el-form-item>
          <el-button type="primary" plain class="addOptionButton" @click="addOption">New option</el-button>
        </template>
        <template v-if="willAddQuestion.type=='text'">
          <el-form-item label="Content">
            <el-input type="textarea"
  :rows="willAddQuestion.row" style="width: 80%" resize="none"></el-input>
          </el-form-item>
          <el-form-item label="Rows">
            <el-input-number v-model="willAddQuestion.row" :min="1" :max="10" label="Description text"></el-input-number>
          </el-form-item>

        </template>
      </el-form>
      <br>
      <div style="width: 100%;text-align: right">
        <el-button style="margin-left: 10px;" @click="dialogShow=false">Cancel</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="checkAddQuestion">Finish</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
  import {designOpera} from './api'
  export default{
    data(){
      return{
        loading:false,// Page loading
        dialogShow:false,
        dialogTitle:'',
        detail:[],
        wjId:0,
        title:'',
        desc:'',
        willAddQuestion:{
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',// Option title
              id:0// Option id
            }
          ],
          row:1,
          must:false,// Whether required?
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
      }
    },
    methods:{
      // Initialize all questions in the questionnaire
      init(wjId,title,desc){
        this.wjId=wjId;
        this.title=title;
        this.desc=desc;
        this.getQuestionList();
      },
      // Get a list of questions (questionnaire content)
      getQuestionList(){
        this.detail=[];
        this.loading=true;
        designOpera({
          opera_type:'get_question_list',
          username:'test',
          wjId:this.wjId,
        })
          .then(data=>{
            console.log(data);
            this.detail=data.detail;
            this.loading=false;
          })
      },
      // Click the Add Question button
      addQuestion(){
        if(this.wjId==0||this.wjId==null){
          this.$message({
            type: 'error',
            message: 'Create a questionnaire first!'
          });
          return;
        }
        this.dialogTitle='Add question';
        this.willAddQuestion={
          id:0,
          type:'',
          title:'',
          options:[
            {
              title:'',// Option title
              id:0// Option id
            }
          ],
          row:1,
          must:false,// Whether required?
        };
        this.dialogShow=true;
      },
      // Delete question
      deleteQuestion(index){
        this.$confirm('Are you sure to delete this question?', 'Remind', {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          designOpera({
            opera_type:'delete_question',
            username:'test',
            questionId:this.detail[index].id,
          })
            .then(data=>{
              console.log(data);
              if(data.code==0){
                this.detail.splice(index,1);
                this.$message({
                  type: 'success',
                  message: 'Successfully deleted!'
                });
              }
              else{
                this.$message({
                  type: 'error',
                  message: data.msg
                });
              }
            })
        });

      },
      // Confirm to add/save topic
      checkAddQuestion(){
        // Add save question
        let newItem={};// Newly added question object
        newItem={
          type:this.willAddQuestion.type,
          title:this.willAddQuestion.title,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,
        };
        newItem.radioValue=-1;
        newItem.checkboxValue=[];
        newItem.textValue='';
        designOpera({
          opera_type:'add_question',
          username:'test',
          wjId:this.wjId,
          questionId:this.willAddQuestion.id,
          title:this.willAddQuestion.title,
          type:this.willAddQuestion.type,
          options:this.willAddQuestion.options,
          row:this.willAddQuestion.row,
          must:this.willAddQuestion.must,

        })
          .then(data=>{
            console.log(data);
            newItem.id=data.id;
            if(data.code==0){
              this.dialogShow=false;
              this.$message({
                type: 'success',
                message: 'Successfully saved!'
              });
              this.getQuestionList();
            }
            else{
              this.dialogShow=false;
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
            this.willAddQuestion={
              id:0,
              type:'',
              title:'',
              options:[''],
              row:1,
              must:false,
            };
          });
      },
      // Click the Edit Question button
      editorQuestion(item){
        this.willAddQuestion.title=item.title;
        this.willAddQuestion.type=item.type;
        this.willAddQuestion.options=JSON.parse(JSON.stringify(item.options));
        this.willAddQuestion.text=item.text;
        this.willAddQuestion.row=item.row;
        this.willAddQuestion.must=item.must;
        this.willAddQuestion.id=item.id;
        this.dialogTitle='Edit question';
        this.dialogShow=true;
      },
      // Add option
      addOption(){
        this.willAddQuestion.options.push({
          title:'',
          id:0,
        });
      },
      // Delete option
      deleteOption(index){
        this.willAddQuestion.options.splice(index,1);
      },
      // Switch question type
      typeChange(value){
        console.log(value);
        this.willAddQuestion.type=value;
        this.willAddQuestion.text='';
        this.row=1;
      },
    }
  }
</script>
<style scoped>
  .Design{

  }
  .Design .dialog{
    text-align: left;
  }
  .Design .questionTitle{
    display: inline-block;
    width: 80%;
    font-size: 16px;
    color: #303133;
  }
  .Design .addOptionButton{
    display: inline-block;
    margin-left: 80px;
  }
  .box-card{
    width: 100%;
    text-align: left;
  }
  .Design .top{
    color: #606266;
    margin-left: 20px;
    padding: 0 10px 10px 10px;
    border-bottom: 3px solid #409EFF;
    font-size: 15px;
    line-height: 22px;
    text-align: left;
  }
</style>
