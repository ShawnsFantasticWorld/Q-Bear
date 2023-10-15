<!--
Program Name: Questionnaire design main page
Function: Design the questionnaire
-->
<template>
  <div class="home">
    <el-row>
      <el-col :span="6">
        <!--Action bar-->
        <div class="opera">
          <el-tooltip class="item" effect="dark" content="Create Questionnaire" placement="bottom">
            <el-button icon="el-icon-plus" type="text" class="rightButton" @click="addWjButtonClick"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="Edit Questionnaire" placement="bottom">
            <el-button icon="el-icon-edit" type="text" class="rightButton" @click="editWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" :content="nowSelect.status==0?'Release Questionnaire':'Pause Questionnaire'" placement="bottom" >
            <el-button :icon="nowSelect.status==0?'el-icon-video-play':'el-icon-video-pause'"  type="text" class="rightButton" @click="pushWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="Preview Questionnaire" placement="bottom">
            <el-button icon="el-icon-view" type="text" class="rightButton" @click="previewWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="Delete Questionnaire" placement="bottom">
            <el-button icon="el-icon-delete" type="text" class="rightButton" @click="deleteWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="Share Questionnaire" placement="bottom">
            <el-button icon="el-icon-share" type="text"class="rightButton" @click="shareWj" :disabled="nowSelect.id==0||nowSelect.id==null"></el-button>
          </el-tooltip>
          <!--<el-tooltip class="item" effect="dark" content="添加模板库" placement="bottom">-->
            <!--<el-button icon="el-icon-upload" type="text"class="rightButton" @click="addTemp"></el-button>-->
          <!--</el-tooltip>-->
        </div>

        <!--Left navigation bar-->
        <el-menu :default-active="defaultActive.toString()" v-loading="loading" class="menu">
          <!--Questionnaire list-->
          <div style="width:100%;text-align: center;font-size: 15px;line-height: 20px;margin-top: 20px;color: #303133" v-if="nowSelect.id==0||nowSelect.id==null">
            Click&nbsp;"+"&nbsp;to create your first questionnaire!
          </div>
          <el-menu-item v-for="(item,index) in wjList" :index="(index+1).toString()" @click="wjClick(item.id,index)">
            <i class="el-icon-tickets"></i>
            <span slot="title" style="display: inline-block">
              {{item.title}}
              <span style="color: #F56C6C;font-size: 13px;" v-if="item.status==0">
                <i class="el-icon-link" style="margin:0;font-size: 13px;color: #F56C6C;width:10px;"></i>
                Unpublished
              </span>
              <span style="color: #67C23A;font-size: 13px;" v-if="item.status==1">
                <i class="el-icon-link" style="margin:0;font-size: 13px;color: #67C23A;width:10px;"></i>
                Published
              </span>
            </span>
          </el-menu-item>
        </el-menu>
      </el-col>

      <el-col :span="18">
        <!--Bookmark page-->
         <el-tabs type="border-card" v-model="activeName">
            <el-tab-pane label="Questionnaire Design" name="wjsj">
              <!--Content area-->
              <div class="content">
                <div v-show="nowSelect.id==0||nowSelect.id==null">Please select a questionnaire first</div>
                <design ref="design" v-show="nowSelect.id!=0&&nowSelect.id!=null"></design>
              </div>
            </el-tab-pane>
            <el-tab-pane label="Results Statistics" name="hdtj">
              <div class="content" ref="pdf">
                <div v-show="nowSelect.id==0||nowSelect.id==null">Please select a questionnaire first</div>
                <data-show ref="dataShow" v-show="nowSelect.id!=0&&nowSelect.id!=null"></data-show>
              </div>
            </el-tab-pane>
          </el-tabs>
      </el-col>
    </el-row>

    <!--Add questionnaire popup-->
    <el-dialog title="Create Questionnaire" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
      <el-form ref="form" :model="willAddWj" label-width="80px">
        <el-form-item label="Title" style="width: 100%;" required>
          <el-input v-model="willAddWj.title" placeholder="Please enter the title of your questionnaire" ></el-input>
        </el-form-item>
        <el-form-item label="Summary" style="width: 100%;">
          <el-input v-model="willAddWj.desc" type="textarea" placeholder="Please enter a questionnaire description" rows="5"></el-input>
        </el-form-item>
      </el-form>
      <div style="width: 100%;text-align: right">
        <el-button style="margin-left: 10px;" @click="openTemp">Create by templates</el-button>
        <el-button style="margin-left: 10px;" @click="dialogShow=false">Cancel</el-button>
        <el-button type="primary" style="margin-left: 10px;" @click="addWj">Confirm</el-button>
      </div>
    </el-dialog>



    <!--Template library popup-->
    <el-dialog title="Templates Library" :visible.sync="tempDialog" :close-on-click-modal="false" class="dialog">
      <el-input placeholder="Enter the keywords to search" prefix-icon="el-icon-search" v-model="tempSearchText"></el-input>
     <el-table :data="tempData" style="width: 100%;" v-loading="tempLoading" element-loading-text="Loadng...">
      <el-table-column prop="tempname" label="Template name" width="250"></el-table-column>
      <el-table-column prop="username" label="Creator"></el-table-column>
       <el-table-column label="Preview">
       <el-link slot-scope="scope" type="primary" @click="lookTempWj(scope.row)">Preview</el-link>
     </el-table-column>
     <el-table-column label="Operate">
        <el-link slot-scope="scope" type="primary" @click="useTemp(scope.row)">Use this template</el-link>
     </el-table-column>
    </el-table>
      <el-pagination layout="prev, pager, next" :total="tempDataCount" @current-change="changeTempPage" :page-size	="5"></el-pagination>
    </el-dialog>


    <!--Share questionnaire pop-up-->
    <el-dialog title="Share questionnaire" :visible.sync="shareDialogShow" :close-on-click-modal="true" class="dialog" @opened="makeQrcode">
      <el-form ref="form" :model="shareInfo" label-width="80px">
        <el-form-item label="Questionnaire link" style="width: 100%;">
          <el-row>
            <el-col :span="16">
              <el-input v-model="shareInfo.url" readonly></el-input>
            </el-col>
            <el-col :span="8">
              <el-button style="margin-left: 5px;" v-clipboard:copy="shareInfo.url" v-clipboard:success="copySuccess" v-clipboard:error="copyError">Copy</el-button>
              <el-button style="margin-left: 5px;" @click="openShareUrl">Open</el-button>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item label="QR Code" style="width: 100%;">
          <canvas id="canvas" style="width: 150px;height: 150px;"></canvas>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>
</template>
<script>
  import {designOpera} from './api'
  import Design from './Design.vue'
  import DataShow from './DataShow.vue'
  import ElButton from "../../node_modules/element-ui/packages/button/src/button";
  import QRCode from 'qrcode'
  export default{
    components:{
      ElButton,
      Design,
      QRCode,
      DataShow,
    },
    data(){
      return{
        defaultActive:1,// Currently active menu
        activeName:'wjsj',// Tab page current selection
        wjList:[],// Questionnaire list
        loading:false,// Whether to display loading
        dialogShow:false,// Whether to display the pop-up window of the questionnaire
        shareDialogShow:false,// Whether to display the pop-up window of the shared questionnaire
        tempDialog:false,// Whether the template library popup window is displayed
//        nowTempData:[],// Current template library page number
        tempData:[],
        tempDataCount:0,
        tempLoading:false,
        tempSearchText:'',
        willAddWj:{
          id:0,
          title:'',
          flag:0,
          desc:'Thanks for participating in our survey! ',
        },
        shareInfo:{
          url:'',
        },

      }
    },
    mounted(){
      this.logincheck();

    },
    computed:{
      // Questionnaire information currently selected
      nowSelect(){
        console.log('nowSelect update');
        let now=this.wjList[this.defaultActive-1];
        if(this.wjList.length==0){
          return {
            id:null,
            title:null,
            desc:null,
            status:null
          }
        }
        return{
          id:now.id,
          title:now.title,
          desc:now.desc,
          status:now.status
        }
      },
    },
    methods:{
      addTemp(){
        designOpera({
          opera_type:'add_temp',
          wjId:107,
        })
          .then(data=>{
            console.log(data);
          })
      },
      // Use questionnaire
      useTemp(item){
        this.tempLoading=true;
        designOpera({
          opera_type:'use_temp',
          wjId:item.tempid,
        })
          .then(data=>{
            console.log(data);
            this.tempLoading=false;
            this.$message({
              type: 'success',
              message: 'Successful use of template!',
              showClose: true
            });
            this.tempDialog=false;
            this.dialogShow=false;
            this.getWjList();

          })
      },
      // Open Questionnaire Library
      openTemp(){
        this.tempDialog=true;
        this.changeTempPage(1);
//        this.getTempWjList();
      },
      // Change template library page number
      changeTempPage(page){
        this.tempLoading=true;
        designOpera({
          opera_type:'get_temp_wj_list',
          page:page
        })
          .then(data=>{
            console.log(data);
            this.tempDataCount=data.count;
            this.tempData=data.detail;
            this.tempLoading=false;
          })
      },
      // Preview Template Questionnaire
      lookTempWj(item){
        let url=window.location.origin+"/tempdisplay/"+item.tempid;//问卷链接
        console.log(url);
        window.open(url);
      },
      // Check if the login has expired
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){// If the returned error is 404, jump to the login page
            this.$message({
              type: 'error',
              message: 'Please login first!',
              showClose: true
            });
            this.$router.push({path:'/login'})
          }
          else{
            this.getWjList();
          }
        })
      },
      // Publish Questionnaire/Pause Questionnaire
      pushWj(){
        let status=1;
        if(this.nowSelect.status==1)
            status=0;
        designOpera({
          opera_type:'push_wj',
          username:'test',
          wjId:this.nowSelect.id,
          status:status
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: status==1?'Successfully released!':'Successfully paused!'
              });
              this.getWjList();
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          })
      },
      // Share questionnaire
      shareWj(){
        if(this.nowSelect.status==0){//问卷未发布
          this.$message({
            type: 'error',
            message: 'Please publish the questionnaire first to share!'
          });
          return;
        }
        this.shareInfo.url=window.location.origin+"/display/"+this.nowSelect.id;//问卷链接
        this.shareDialogShow=true;
      },
      // Generate QR code
      makeQrcode(){
        var canvas=document.getElementById('canvas');
        QRCode.toCanvas(canvas,this.shareInfo.url);
      },
      // Copy and share link successfully
      copySuccess(e){
        console.log(e);
        this.$message({
          type: 'success',
          message: 'Copied link to clipboard!'
        });
      },
      // Failed to copy and share link
      copyError(e){
        console.log(e);
        this.$message({
          type: 'error',
          message: 'Copy failed'
        });
      },
      // Open share link
      openShareUrl(){
        window.open(this.shareInfo.url);
      },
      // Preview questionnaire
      previewWj(){
        let url=window.location.origin+"/display/"+this.nowSelect.id;//问卷链接
        console.log(url);
        window.open(url);
      },
      // Edit questionnaire
      editWj(){
        this.dialogShow=true;
        this.willAddWj=this.nowSelect;
      },
      // Add questionnaire button click
      addWjButtonClick(){
        this.dialogShow=true;
        this.willAddWj={
          id:0,
          title:'',
          flag:0,
          desc:'Thanks for participating in our survey! ',
        };
      },
      // Add questionnaire
      addWj(){
        if (this.willAddWj.title == ''){
          this.$message({
            type: 'error',
            message: 'The title can not be blank'
          });
          return;
        }
        designOpera({
          opera_type:'add_wj',
          username:'test',
          title:this.willAddWj.title,
          id:this.willAddWj.id,
          desc:this.willAddWj.desc,
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: 'Saved!'
              });
              this.getWjList();
            }
            else{
              this.$message({
                type: 'error',
                message: data.msg
              });
            }
          });
        this.dialogShow=false;
        this.willAddWj.title='';
      },
      // Get list of questionnaires
      getWjList(){
        this.loading=true;
        designOpera({
          opera_type:'get_wj_list',
          username:'test'
        })
          .then(data=>{
            console.log(data);
            this.wjList=data.data.detail;
            this.loading=false;
            // Get the currently selected questionnaire topic
            this.lookDetail();
          })
      },
      // Delete questionnaire
      deleteWj(){
        this.$confirm('Confirm delete'+this.nowSelect.title+'? It cannot be restored after deletion!', 'remind', {
          confirmButtonText: 'Confirm',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.loading=true;
          designOpera({
          opera_type:'delete_wj',
          username:'test',
          id:this.nowSelect.id
        })
          .then(data=>{
            console.log(data);
            if(data.code==0){
              this.$message({
                type: 'success',
                message: 'Successfully deleted!'
              });
              this.loading=false;
              this.getWjList();
              this.defaultActive=1;
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
      // Questionnaire click
      wjClick(id,index){
        this.defaultActive=(index+1).toString();
        this.lookDetail();
      },
      // View Questionnaire Details
      lookDetail(){
        this.$refs.design.init(this.nowSelect.id,this.nowSelect.title,this.nowSelect.desc);
        console.log("id=")
        console.log(this.nowSelect.id)
        this.$refs.dataShow.dataAnalysis(this.nowSelect.id);
      },
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
    padding: 20px;
    padding-right: 50px;
    height: calc(100vh - 175px);
    text-align: center;
    overflow-y: scroll;
    overflow-x: hidden;
  }
  .menu{
    background-color: white;
    height: calc(100vh - 100px);
    overflow-x: scroll;
    overflow-y: scroll;
    left: 0;
  }
  .home .opera{
    position: relative;
    background-color: #fafafa;
    text-align: center;
    height: 40px;
  }
  .home .rightButton{
    font-size: 16px;
  }
  .home .addWjDiv{
    height: 50px;line-height: 50px;text-align: center;
    border-bottom: 1px solid #eee
  }
</style>
