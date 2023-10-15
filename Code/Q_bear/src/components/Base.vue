<!--
Program: Website Navigation Bar
Function: Website Top Navigation Bar
-->
<template>
  <div class="main">
    <el-container>
      <el-header>
        <div class="logo" @click="toIndex">
          <img src="/static/images/logo.png" class="logoImg">
          <span style="color: #303133">Q-Bear</span>
          <span style="font-size: 13px;margin-left: 5px;color: #606266">——Free Online Questionnaire System</span>
        </div>
        <div style="float: right;margin-right: 50px;line-height: 60px;">
          <!-- Show when not logged in -->
          <template v-if="!showname">
            <el-button type="primary" plain style="font-size: 15px;" @click="toLogin">Login</el-button>
            <el-button plain style="font-size: 15px;" @click="toRegiste">Register</el-button>
          </template>
          <!-- Show when logged in -->
          <template v-else>
            <!-- Successful login, display username -->
            <el-dropdown trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                {{username}}<i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <!-- Sign out -->
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="a">Questionnaire Management</el-dropdown-item>
                <el-dropdown-item command="b">Logout</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </div>
      </el-header>
      <el-main style="padding: 0">
        <router-view @state="state"/>
      </el-main>
    </el-container>
  </div>
</template>
<script>
  import {designOpera} from './api'
  export default {
    name:'Base',
    data: function () {
      return {
        showname: false, // Display state of login, register button
        username:''  // Username
      }
    },
    methods:{
      toIndex(){
        this.$router.push({path:'/index'});
      },
      //Check if the login has expired
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){
            return false
          }
          else if(data.data!=null){
            console.log(data)
            sessionStorage.setItem('username',data.data.user) // Save the username passed by the backend into the session
          }
          this.state()  // Call the state method
        })
      },
      // Method: Jump to the questionnaire management page
      toHome(){
        this.$router.push({path:'/home'})
      },
      // Method: Jump to login page
      toLogin(){
        this.$router.push({path:'/login'})
      },
      // Method: Jump to register page
      toRegiste(){
        this.$router.push({path:'/register'})
      },
      // Determine whether there is data in the session, if there is, set showname to true, otherwise false
      state(){
        console.log('state')
        console.log(sessionStorage.getItem('username'))
        if(sessionStorage.getItem('username')!=null){
          this.showname=true;
          this.username = sessionStorage.getItem('username')
        }
        else {
          this.showname = false
        }
      },
      // Drop down menu operation
      handleCommand(command){
        if(command=='a'){
          this.toHome();
        }
        else if(command=='b'){
          this.exit();
        }
      },
      // Sign out
      exit(command){
        designOpera({
          opera_type:'exit',  // Operation type
          username:sessionStorage.getItem('username')  // Get the username in the session
        })
        .then(data=>{
          console.log(data);
          if(data.code==0){
            sessionStorage.clear()  // Log out successfully, clear session
            this.state()  // Call the state method
            this.toLogin()  // Call the toLogin method
          }
          else{
            this.$message({  // Error message
              type: 'error',
              message: 'Network Error!',
              showClose: true
            });
          }
        })
      }
    },
    // Page initialization
    mounted(){
      this.logincheck();
    },
  }
</script>
<style scoped>
  .main{
    position: absolute;
    width: 100%;
    height: 100%;
  }
  /* logo image style */
  .logoImg{
    width: 30px;
    vertical-align: middle;
  }
  /* logo box style */
  .logo{
    height: 60px;
    display: inline-block;
    line-height: 60px;
    font-size: 20px;
    position: absolute;
    left: 100px;
    color: #303133;
    cursor: pointer;
  }
  .el-header{
    border-bottom: 2px solid #409EFF;
    background-color: white;
  }
   .el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
  .demonstration {
    display: block;
    color: #8492a6;
    font-size: 14px;
    margin-bottom: 20px;
  }
</style>
