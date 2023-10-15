<template>
  <div class="Count">
    <el-card class="question" v-for="(item,index) in detail">
      <div slot="header" class="clearfix">
        <span>{{(index+1)+'.'+item.title}}</span>
        <el-button style="float: right; padding: 3px 0" type="text">Action Button</el-button>
      </div>
      <div>
        <el-table :data="item.result" style="width: 100%" stripe class="table">
          <el-table-column prop="option" label="Options" width="180"></el-table-column>
          <el-table-column prop="count" label="Quantity" width="180"></el-table-column>
          <el-table-column prop="percent" label="Proportion"></el-table-column>
        </el-table>
        <div :id="'img'+(index)" class="img">

        </div>
      </div>
    </el-card>
  </div>
</template>
<script>
  import echarts from 'echarts'
  export default{
    data(){
      return{
        detail:[
          {
            title:'Your gender？',
            type:'radio',
            result:[
              {
                option:'Male',
                count:5,
                percent:50
              },
              {
                option:'Female',
                count:5,
                percent:50
              },
            ]
          },
          {
            title:'How much do you spend on daily necessities on average every month?',
            type:'radio',
            result:[
              {
                option:'Under 50',
                count:0,
                percent:0
              },
              {
                option:'50-100',
                count:2,
                percent:66.67
              },
              {
                option:'100-150',
                count:1,
                percent:33.33
              },
              {
                option:'Beyond 150',
                count:0,
                percent:0
              },
            ]
          },
        ]
      }
    },
    mounted(){
      this.init();
    },
    methods:{
      init(){
        for(let i=0;i<this.detail.length;i++){
          this.setImg(i);
        }
      },
      setImg(id){
        console.log(id);
        var myChart = echarts.init(document.getElementById('img'+id));
        var option = {
            tooltip: {},
            legend: {
                data:['Quantity']
            },
            dataset:{
              dimensions: ['option', 'count', 'percent'],
              source: this.detail[id].result,
            },
            xAxis: {
                type:'category'
            },
            yAxis: {},
            series: [
              {
                type: 'bar',
                barWidth:30,

//                label:{
//                    show:true,
//                formatter:'{b}xxx'
//
//                }
              },
            ],
        };
        myChart.setOption(option);
      }
    }
  }
</script>
<style scoped>
  .Count{
    background-color: yellow;
    text-align: center;
    /*width: 80%;*/
  }
  .Count .question{
    /*background-color: red;*/
    max-width: 800px;
    width: 80%;
    display: inline-block;
    margin: 10px;
    text-align: left;
  }
  .Count .table{
    /*width: 100px;*/
  }
  .Count .img{
    width: 100%;
    height: 300px;
    /*background-color: green;*/
  }

</style>
