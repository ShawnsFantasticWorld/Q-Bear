<!--
Program Name：Data analysis page
Function：Analyze the data of the survey results and visualize them with charts
-->
<template>
  <div
    id="pdfDom"
    class="Count"
    v-loading="loading"
    element-loading-text="Generating..."
  >
    <div v-if="!(detail.length == 0)" class="opera-buttons">
      <el-button
        type="primary"
        size="mini"
        @click.native="analysisExportExcel"
        :loading="exportExcelLoading"
        >Export in excel</el-button
      >
      <el-button type="success" size="mini" @click.native="exportPdf"
        >Export in PDF</el-button
      >
    </div>
    <div v-if="detail.length == 0">Temporarily no data</div>
    <el-card class="question" v-for="(item, index) in detail">
      <div slot="header" class="clearfix">
        <span>{{ index + 1 + "." + item.title }}</span>
      </div>
      <!--If the question type in the database is single choice or multiple choice-->
      <!--Then display the data in the database in the form of tables, histograms, pie charts, donut charts, and bar charts-->
      <div v-if="item.type == 'radio' || item.type == 'checkbox'">
        <el-table
          size="small"
          :data="item.result"
          style="width: 100%"
          stripe
          class="table"
        >
          <el-table-column prop="option" label="Options"></el-table-column>
          <el-table-column
            prop="count"
            label="Quantity"
            width="180"
          ></el-table-column>
          <el-table-column
            prop="percent"
            label="Proportion"
            width="180"
          ></el-table-column>
        </el-table>
        <br />

        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 1)"
          >Histogram</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 2)"
          >Pie chart</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 3)"
          >Donut chart</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 4)"
          >Bar chart</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="changeValue(index, 0)"
          >Hide chart</el-button
        >

        <div :id="'img' + index" class="img" v-show="visible[index] == 1"></div>
        <div
          :id="'bing' + index"
          class="bing"
          v-show="visible[index] == 2"
        ></div>
        <div
          :id="'ring' + index"
          class="ring"
          v-show="visible[index] == 3"
        ></div>
        <div :id="'tz' + index" class="tz" v-show="visible[index] == 4"></div>
      </div>
      <!--If the question type in the database is text type, the data will be displayed in the form of a pop-up window-->
      <div v-if="item.type == 'text'">
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="lookTextDetail(item.questionId)"
          >Details</el-button
        >
        <el-button
          size="mini"
          type="primary"
          plain
          @click.native="answerText2Excel(item.questionId)"
          :loading="item.questionId == answerText2ExcelQeustionId"
          >Export excel</el-button
        >
      </div>
    </el-card>
    <el-dialog title="Details" :visible.sync="dialogTableVisible">
      <el-table :data="tableData">
        <el-table-column property="context" label="Answers"></el-table-column>
      </el-table>
      <el-pagination
        @size-change="sizeChange"
        @current-change="currentChange"
        :current-page.sync="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size.sync="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-dialog>
  </div>
</template>
<script>
import echarts from "echarts";
import { designOpera } from "./api";
import Design from "./Design.vue";
import axios from "axios";

export default {
  data() {
    return {
      dialogTableVisible: false,
      visible: [],
      loading: false,
      detail: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      questionId: 0,
      wjId: 0,
      exportExcelLoading: false,
      answerText2ExcelQeustionId: 0
    };
  },
  mounted() {
    //      this.dataAnalysis()
    //      console.log(this.visible);
  },
  methods: {
    answerText2Excel(questionId) {
      this.answerText2ExcelQeustionId = questionId;
      designOpera({
        opera_type: "answer_text_to_excel",
        questionId: questionId
      }).then(data => {
        this.doDownload(data.b64data, data.filename, "excel");
        this.answerText2ExcelQeustionId = 0;
      });
    },
    // Export in pdf
    exportPdf() {
      this.$alert("Developing...", "Remind");
    },
    // Export in excel
    analysisExportExcel() {
      this.exportExcelLoading = true;
      designOpera({
        opera_type: "analysis_export_excel",
        wjId: this.wjId
      }).then(data => {
        this.doDownload(data.b64data, data.filename, "excel");
        this.exportExcelLoading = false;
      });
    },
    doDownload(data, filename, type) {
      var b64data = data; // Base64 data
      // b64data = b64data.replace("data:" + type + ";base64,", "");
      var bdata = this.dataURLtoBlob(b64data);
      if (!b64data) {
        return;
      }
      let url = window.URL.createObjectURL(new Blob([bdata]));
      let link = document.createElement("a");
      link.style.display = "none";
      link.href = url;
      //        link.download = 'ea7c0cf24153e0cd62bc8b64841fd84d.jpg'; // Downloaded file name
      link.setAttribute("download", filename);

      document.body.appendChild(link);
      link.click();
    },
    dataURLtoBlob(dataurl) {
      //          dataurl=dataurl.replace('data:application/json;base64,','')
      console.log(dataurl);
      var bstr = atob(dataurl),
        n = bstr.length,
        u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return u8arr;
    },
    // Get form data
    getTableData() {
      designOpera({
        opera_type: "get_text_answer_detail",
        questionId: this.questionId,
        currentPage: this.currentPage,
        pageSize: this.pageSize
      }).then(data => {
        console.log(data);
        this.tableData = data.detail;
        this.total = data.total;
      });
    },
    sizeChange() {
      this.getTableData();
    },
    currentChange() {
      this.getTableData();
    },
    // View text answer details
    lookTextDetail(questionId) {
      this.tableData = [];
      this.pageSize = 10;
      this.total = 0;
      this.currentPage = 1;
      this.dialogTableVisible = true;
      this.questionId = questionId;
      this.getTableData();
    },
    // Change chart type
    changeValue(num, value) {
      this.$set(this.visible, num, value);
      console.log("num=" + num);
      console.log("value=" + value);
      if (value == 1) {
        this.setImg(num);
      } else if (value == 2) {
        this.setPar(num);
      } else if (value == 3) {
        this.setRing(num);
      } else if (value == 4) {
        this.setTz(num);
      }
    },
    // Request backend data
    dataAnalysis(id) {
      this.loading = true;
      this.detail = [];
      console.log("wjid===");
      console.log(this.wjId);
      this.wjId = id;
      designOpera({
        opera_type: "dataAnalysis",
        username: "test",
        wjId: id
      }).then(data => {
        console.log(data);
        console.log(data.detail);
        this.detail = data.detail;
        this.visible = [];
        this.loading = false;
      });

      this.dialogShow = false;
    },
    test() {
      console.log(this.visible);
    },

    // Histogram
    setImg(id) {
      console.log(id);
      console.log(this.detail[id].result);
      let myChart = echarts.init(document.getElementById("img" + id));
      var option = {
        tooltip: {},
        legend: {
          data: ["Quantity"]
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        xAxis: {
          type: "category"
        },
        yAxis: {},
        series: [
          {
            name: "Quantity:",
            type: "bar",
            barWidth: 30,
            color: "deepskyblue"
          }
        ]
      };
      myChart.setOption(option);
    },
    // Pie chart
    setPar(id) {
      let myChart = echarts.init(document.getElementById("bing" + id));
      var option = {
        tooltip: {},

        color: ["#409EFF", "#FFB54D", "#FF7466", "#44DB5E"],
        legend: {
          data: ["Quantity"]
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        series: [
          {
            name: "Statistical results:",
            type: "pie",
            radius: "55%",
            center: ["50%", "50%"],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    // Donut chart
    setRing(id) {
      //console.log(id);
      let myChart = echarts.init(document.getElementById("ring" + id));
      var option = {
        tooltip: {},
        legend: {},
        color: ["#409EFF", "#FFB54D", "#FF7466", "#44DB5E"],
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        series: [
          {
            name: "Quantity:",
            type: "pie",
            radius: ["50%", "70%"],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: "center"
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: "30",
                  fontWeight: "bold"
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    // Bar chart
    setTz(id) {
      //console.log(id);
      let myChart = echarts.init(document.getElementById("tz" + id));
      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        dataset: {
          dimensions: ["option", "count", "percent"],
          source: this.detail[id].result
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          type: "value",
          boundaryGap: [0, 0.01]
        },
        yAxis: {
          type: "category"
        },
        series: [
          {
            name: "Quantity:",
            type: "bar",
            barWidth: 30,
            color: "#409EFF"
          }
        ]
      };
      myChart.setOption(option);
    },
    // Text content
    setText(id) {
      return {
        resule: this.detail[id].result
      };
    }
  }
};
</script>
<style scoped>
.Count {
}
.Count .question {
  max-width: 800px;
  width: 80%;
  display: inline-block;
  margin: 5px;
  text-align: left;
}
.Count .table {
}
.Count .img {
  width: 500px;
  height: 300px;
}
.Count .bing {
  width: 500px;
  height: 300px;
}
.Count .ring {
  width: 500px;
  height: 300px;
}
.Count .tz {
  width: 500px;
  height: 300px;
}
.opera-buttons {
  padding: 10px;
}
</style>
