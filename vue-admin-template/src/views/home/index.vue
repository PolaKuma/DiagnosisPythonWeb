<template>
  <div class="hello">
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="grid-content bg-purple">
          <!-- 首页user信息 -->
          <el-card shadow='hover'>
            <div class="userCard">
              <el-avatar :size="150" :src=imgUrl></el-avatar>
              <div class="userInfo">
                <p class="important-font" v-text="name"></p>
                <p class="secondary-font">管理员</p>
              </div>
            </div>
            <div class="login-info">
              <p>入职日期: 2022/07/06 18:16</p>
            </div>
          </el-card>
          <!-- 首页表格 -->
          <el-card shadow='hover' class="tableInfo">
            <div slot="header">
              <span class="important-font">客户信息</span>
            </div>
            <div>
              <el-table
                  :data="tableData"
                  stripe
                  border
                  height="320px"
                  style="width: 100%">
                <el-table-column
                    prop="date"
                    label="日期"
                    width="120">
                </el-table-column>
                <el-table-column
                    prop="name"
                    label="姓名"
                    width="80">
                </el-table-column>
                <el-table-column
                    prop="address"
                    label="地址">
                </el-table-column>
              </el-table>
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col :span="16">
        <!-- 两个订单信息 -->
        <div class="num">
          <el-card shadow='hover' v-for="item in countData" :key="item.name"
                   :body-style="{ display: 'flex',padding: 0 }" class="OrderCard">
            <i class="icon" :class="'el-icon-'+item.icon" :style="{ background: item.color}"></i>
            <div>
              <p class="important-font numa">￥{{ item.value }}</p>
              <p class="secondary-font numa">{{ item.name }}</p>
            </div>
          </el-card>
        </div>
        <!-- 柱状图 -->
        <el-card style="height: 280px">
          <div style="height:280px;" ref="barEcharts">{{ initBarEcharts() }}</div>
        </el-card>
        <div class="num graph">
          <el-card style="width:100%;">
            <div style="">
              <el-calendar v-model="value"></el-calendar>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "Index",
  data() {
    return {
      name: 'admin',
      imgUrl: require('@/assets/img/head_portrait1.jpg'),
      value: new Date(),
      tableData: [{
        date: '2016-05-03',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-02',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-04',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-01',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-08',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-06',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }, {
        date: '2016-05-06',
        name: '王小虎',
        address: '上海市普陀区金沙江路 1518 弄'
      }],
      countData: [
        {
          name: '今日支付订单',
          value: 1200,
          icon: 'success',
          color: '#2ec7c9'
        },
        {
          name: '今日收藏订单',
          value: 1200,
          icon: 'star-on',
          color: '#ffb980'
        }
      ]
    }
  }, methods: {
    //柱状图
    initBarEcharts() {
      // 新建一个promise对象
      let p = new Promise((resolve) => {
        resolve()
      })
      //然后异步执行echarts的初始化函数
      p.then(() => {
        //	此dom为echarts图标展示dom
        let myChart = echarts.init(this.$refs.barEcharts)
        let option = {
          title: {
            text: '销售表'
          },
          tooltip: {},
          legend: {
            data: ['今日销量', '昨日销量']
          },
          xAxis: {
            data: ['华为', 'vivo', 'oppo', 'ipone', '小米', '三星']
          },
          yAxis: {},
          series: [
            {
              name: '今日销量',
              type: 'bar',
              data: [5, 20, 36, 10, 10, 20]
            },
            {
              name: '昨日销量',
              type: 'bar',
              data: [10, 18, 34, 8, 12, 21]
            }
          ]
        }
        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      })
    },
    //饼图
    initPieEcharts() {
      let p = new Promise((resolve) => {
        resolve()
      })
      //然后异步执行echarts的初始化函数
      p.then(() => {
        let myChart = echarts.init(this.$refs.pieEcharts);
        let option = {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '0%',
            left: 'left'
          },
          series: [
            {
              name: '订单信息',
              type: 'pie',
              radius: ['20%', '65%'],
              avoidLabelOverlap: false,
              label: {
                show: false,
                position: 'left'
              },
              labelLine: {
                show: false,
              },
              data: [
                {value: 1048, name: '成交订单量'},
                {value: 735, name: '退款订单量'},
                {value: 580, name: '浏览量'},
                {value: 484, name: '加购量'},
                {value: 300, name: '预购量'}
              ]
            }
          ]
        }
        myChart.setOption(option);
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less" scoped>
.el-card__body {
  padding: 10px;
}

.userCard {
  height: 180px;
  display: flex;
  border-bottom: 2px solid #DCDFE6;
  border-radius: 2px;
}

.userInfo {
  width: auto;
  padding: 6% 0 0 6%;
}

.important-font {
  font-weight: 900;
  font-size: 30px;
}

.secondary-font {
  color: #909399;
}

.login-info {
  height: 40px;
  text-align: left;
  color: #909399;
}

.tableInfo {
  margin: 20px 0 0 0;
}

.OrderCard {
  margin: 0;
  height:50px !important;
  border: #DCDFE6 1px solid;
  border-radius: 10px;

  i {
    width: 30%;
    line-height: 120px;
    font-size: 10px;
    color: #fff;
  }

  div {
    width: 300px;
  }
}

.el-card {
  border: none;
}

.num {
  display: flex;
  flex-wrap: wrap;
}

.graph {
  margin: 15px 0 0 0;
}

.el-calendar {
  height: 265px;
}

.hello{
  background-color: white !important;
}
</style>
