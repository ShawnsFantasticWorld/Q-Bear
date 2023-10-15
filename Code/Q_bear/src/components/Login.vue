<!--
Program Name: Website login page
Function: Entrance to the site
-->
<template>
  <div class="login">
    <div class="main_login">
      <div class="title">Login</div>
      <el-row type="flex" justify="center">
        <!-- Login form -->
        <el-form ref="loginForm" :rules="rules" :model="loginForm">
            <el-form-item prop="username">
                <el-input @keyup.enter.native="login('loginForm')" icon="el-icon-search" placeholder="Please Enter Your UserName" v-model="loginForm.username">
                  <i class="el-icon-user" slot="prefix"> </i>
                </el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input @keyup.enter.native="login('loginForm')" placeholder="Please Enter Your Password" v-model="loginForm.password" show-password>
                  <i class="el-icon-lock" slot="prefix"> </i>
                </el-input>
            </el-form-item>
            <!-- Login button -->
            <el-form-item>
              <el-button type="primary" @click="login('loginForm')" style="text-align: center;width: 150px">Login</el-button>
            </el-form-item>
          </el-form>
      </el-row>
      <!-- Register and Forgot Password Links -->
      <div class="link">
        <el-link type="primary" :underline="false" href="/register">Create New Account</el-link>
        <!-- <el-link type="primary" :underline="false" href="/resetpass">Forget My Password</el-link> -->
      </div>
    </div>
  </div>
</template>
<script>
  import {designOpera} from './api'
  import { Loading } from 'element-ui';
export default {
  name: 'Login',
  data() {
    return {
      // Form data
      loginForm: {
        username: '',  // Username
        password: '',  // Password
      },
      rules: {
        // Form Validation (Username Validation Rules)
        username: [
          {required: true,message: 'Account cannot be empty', trigger: 'blur'},
          { max: 20, message: 'Account length up to 20 characters', trigger: 'blur' }
        ],
        // Form Validation (Password Validation Rules)
        password: [
          {required: true, message: 'Password can not be blank', trigger: 'blur'},
          { min: 6, message: 'The password length must be at least 6 characters', trigger: 'blur' }
        ],
      },
    }
  },
// Page initialization
  mounted() {
    this.logincheck();
  },
// Method definition
  methods: {
    // Check if the login has expired
      logincheck(){
          designOpera({
          opera_type:'logincheck',
        })
        .then(data=>{
          console.log(data);
          if(data.code==404){
            this.$router.push({path:'/login'})
          }
          if(data.data!=null){
            console.log(data)
            sessionStorage.setItem('username',data.data.user) // Save the username passed by the backend into the session
            this.$router.push({path:'/home'})
          }
        })
      },
    // Login Method
    login(formName) {
      // The form is verified and can be operated
      this.$refs[formName].validate((valid) => {
        if (valid) {
          designOpera({
            opera_type:'login',  // Operation type
            username:this.loginForm.username,  // Username
            password:this.$md5(this.loginForm.password),  // Password md5 encryption
          })
            .then(data=>{
              console.log(data);
              if (data.code==0) {  // Login is successful, and prompt
                this.$notify({
                  type: 'success',
                  message: 'Welcome,' + this.loginForm.username + '!',
                  duration: 3000
                });
                this.$router.push({path:'/home'});  // Jump to the user home page
                sessionStorage.setItem("username",this.loginForm.username)   // Store the username in the session
                this.$emit("state");  // Pass state to base page
              }
              else {
                if(data.code==-5){  // Not registered, friendly reminder not registered
                    this.$message({
                    type: 'error',
                    message: 'You have not registered an account, please register',
                    showClose: true
                  });
                }
                else { // Account or password error prompt
                    this.$message({
                    type: 'error',
                    message: 'Incorrect username or password',
                    showClose: true
                  });
                }
              }
            })
        } else {
          return false;  // Form validation error returns false
        }
      })
    },
  }
}
</script>

<style scoped>
  /* main page style */
  .login {
    position: absolute;  /* absolute positioning */
    width:100%;
    height:100%;
    background-color: #E4E7ED;
  }
/* title style */
  .title {
    font-size: large;  /*font size*/
    font-weight: bolder;  /*bold font*/
    text-align: center;
    color:black;
  }
/* login section div style */
  .main_login {
    position: absolute;
    left:48%;
    top:40%;
    width:320px;
    height:250px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px;  /*rounded border*/
    background: #F2F6FC;
  }
  /* form style */
  .el-form {
    padding-top: 5%;
    padding-left: 10%;
    padding-right: 10%;
    width:280px;
  }
  /* .el-row label style */
  .el-row {
    height: 100%;
    width: 100%;
  }
  /* text link div style */
  .link{
    margin-top: -13%;
    text-align: center;   /* center text */
    margin-left: -5%;
  }
  /* text link style */
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }
</style>
