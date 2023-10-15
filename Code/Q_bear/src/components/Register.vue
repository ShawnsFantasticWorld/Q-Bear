<!--
Program Name: Website registration page
Function: Website registration
-->
<template>
    <div class="register">
      <div class="main-register">
        <div class="title">Create A New Account</div>
        <!-- registration form -->
        <el-row>
          <el-form  :model="registerForm" status-icon :rules="rules" size="medium" ref="registerForm" label-width="100px" class="demo-registeForm">
            <el-form-item prop="username" label="Username">
              <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.username" placeholder="Please Enter Your Username"></el-input>
            </el-form-item>
            <el-form-item label="Password" prop="pass">
              <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.pass" autocomplete="off" placeholder="Password(No less than 6 digits)" show-password>
              </el-input>
            </el-form-item>
            <el-form-item label="Confirm" prop="checkPass">
              <el-input  @keyup.enter.native="Register('registerForm')" v-model="registerForm.checkPass" autocomplete="off" placeholder="Enter Your Password Again" show-password>
              </el-input>
            </el-form-item>
            <!-- 注册，重置按钮 -->
            <el-form-item style="margin-left: -25%">
              <el-button type="primary" @click="Register('registerForm')" >Sign up</el-button>
              <el-button @click="resetForm('registerForm')" style="margin-right: -5%">Reset</el-button>
            </el-form-item>
          </el-form>
        </el-row>
        <!-- login page link -->
        <div class="link">
        <el-link type="primary" :underline="false" href="/login">Sign in instead?</el-link>
      </div>
      </div>
    </div>
</template>

<script>
    import { designOpera } from './api';
    export default {
    name: "Register",
    data() {
      // check password
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Please enter password'));
        } else {
          if (this.registerForm.checkPass !== '') {
            this.$refs.registerForm.validateField('checkPass');
          }
          callback();
        }
      };
      // Confirm Password Verification
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('Confirm your password'));
        } else if (value !== this.registerForm.pass) {
          callback(new Error('The passwords entered twice are inconsistent!'));
        } else {
          callback();
        }
      };
      return {
        // form data
        registerForm: {
          username: '', // Username
          pass: '', // Password
          checkPass: '',  // check password
        },
        // validation rules
        rules: {
          // Username Validation Rules
          username: [
          {required: true,message: 'Account cannot be empty', trigger: 'blur'},
          { max: 20, message: 'Account length up to 20 characters', trigger: 'blur' }
        ],
        // Password Validation Rules
        pass: [
          { required: true, validator: validatePass, trigger: 'blur' },
          { min: 6, message: 'The password length must be at least 6 characters', trigger: 'blur' },
          {max:16,message:'Password length cannot exceed 16 characters',trigger:'blur'}
        ],
        // Check password validation rules
        checkPass: [
          { required: true, validator: validatePass2, trigger: 'blur' }
        ],
        },
      };
    },
    // page initialization
     mounted() {
       this.logincheck();
    },
    // method definition
    methods: {
      // Check if the login has expired
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
            sessionStorage.setItem('username',data.data.user) //将后端传的username存入session
            this.$router.push({path:'/home'})
          }
        })
      },
      // register
      Register(formName) {
        // The form is verified and can be operated
        this.$refs[formName].validate((valid) => {
          if (valid) {
            designOpera({
              opera_type:'register',  //operation type
              username:this.registerForm.username,  //username
              password:this.$md5(this.registerForm.pass)  //password md5 encryption
            })
            .then(data=>{
              console.log(data);
              if(data.code == 0){ //registration success
                  this.$message({
                  message: 'Registration is successful, please log in!',
                  type: 'success'
                });
                this.$router.push({path:'/login'});
              }
              else{   //registration failed
                this.$message({
                    type: 'error',
                    message: 'This username has been registered',
                    showClose: true
                  });
              }
            });
          } else {   //Form validation failed, return false
            console.log('error submit!!');
            return false;
          }
        });
      },
      // form reset
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
    }
}
</script>

<style scoped>
  /* Registration page style */
  .register{
    position: absolute;
    width:100%;
    height:100%;
    background-color: #E4E7ED;
  }
  /* title style */
  .title {
    font-size: large;
    font-weight: bolder;
    text-align: center;
    color:black;
  }
  /* Registration Form Area Styles */
  .main-register {
    position: absolute;
    left:48%;
    top:40%;
    width:350px;
    height:300px;
    margin:-190px 0 0 -190px;
    padding:40px;
    border-radius: 5px;  /*圆角边框*/
    background: #F2F6FC;
  }
  /* el-form label style */
  .el-form {
    padding-top: 5%;
    padding-right: 10%;
  }
  /* el-form-item label style */
  .el-form-item{
    margin-left: -10%;
  }
  /* el-row label style */
  .el-row {
    height: 100%;
    width: 100%;
  }
  /* link label style */
  .link{
    margin-top: -12%;
    text-align: center;
    margin-left: -5%;
  }
  /* el-link label style */
  .el-link{
    margin-left: 8px;
    line-height: 20px;
    font-size: 8px;
  }

</style>
