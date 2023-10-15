<!--
Program Name: Home page
Function: Introduce the site
-->
<template>
  <div class="main">
    <el-carousel height="500px">
      <el-carousel-item v-for="(item, index) in topImg" :key="index">
        <!--<div style="background-color: black;width: 100%;height: 100%;">-->
        <img :src="item.url" style="width: 100%;height: 100%;" />
        <div class="cover">
          {{ item.title }}<br />
          <span style="font-size: 35px">{{ item.subTitle }}</span>
        </div>
      </el-carousel-item>
    </el-carousel>
    <!--<el-divider></el-divider>-->

    <!-- <code-div><img src="/static/images/demo1.png" class="demoImg"/></code-div>
    <code-div><img src="/static/images/demo2.png" class="demoImg"/></code-div>
    <code-div><img src="/static/images/demo3.png" class="demoImg"/></code-div> -->
    <!-- <img src="/static/images/demo1.png" class="demoImg" /><br /> -->
    <!-- <img src="/static/images/demo2.png" class="demoImg" /><br />
    <img src="/static/images/demo3.png" class="demoImg" /><br /><br /> -->
    <h3>NOTICE TO USER:</h3>

    <el-divider></el-divider>
    <div style="text-align: left;padding-left: 300px;padding-right: 300px;">
      <p>
        The following content is prohibited on this platform:
      </p>
      <p class="b">1. Prohibit hate speech</p>
      <p class="b">
        2. Prohibition of posting advertising content
      </p>
    </div>
    <el-footer class="bottom">
      <p>By: Jiajun Sun & Xianchun Zeng</p>
      <p>CSE 503 Creative Project</p>
    </el-footer>
  </div>
</template>
<script>
import CodeDiv from "@/components/CodeDiv";
export default {
  components: {
    CodeDiv
  },
  data() {
    return {
      topImg: [
        {
          title: "Q-BEAR",
          subTitle: "Free Online Questionnaire System",
          url: "/static/images/4.jpg"
        }
      ]
    };
  }
};
</script>
<style scoped>
.main {
  position: relative;
  width: 100%;
  height: 100%;
}
.bottom {
  height: 150px !important;
  background-color: #2e3e4e;
  color: #9b9ea0;
  position: relative;
  padding: 20px;
}
.demoImg {
  width: 100%;
  height: 100%;
  /*border-radius: 5px;*/
}
.cover {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 100;
  left: 0;
  top: 0;
  color: white;
  font-size: 50px;
  line-height: 60px;
  padding-top: 180px;
}
.lj {
}
.b {
  font-weight: 700;
}
</style>
