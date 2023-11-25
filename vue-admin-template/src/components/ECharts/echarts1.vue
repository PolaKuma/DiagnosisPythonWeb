<template>
  <!-- Echarts容器 -->
  <div style="width: auto; height: 470px" id="echarts1"></div>
</template>

<script>
import echarts from 'echarts'

const colors = ['#5470C6', '#EE6666']
export default {
  name: 'echarts1',
  data() {
    return {
      // Echarts配置项
      option: {
        color: colors,
        tooltip: {
          trigger: 'none',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {},
        grid: {
          top: 70,
          bottom: 50,
          left: 0,
          right: 0
        },
        // X轴配置
        xAxis: [
          {
            type: 'category',
            axisTick: {
              alignWithLabel: true
            },
            data: this.generateXAxisData('2023')
          }
        ],
        // Y轴配置
        yAxis: [
          {
            type: 'value'
          }
        ],
        // 系列数据配置
        series: [
          this.generateSeriesData('阴性', [2, 6, 9, 26, 28, 70, 175, 60, 48, 18, 6, 2], 0),
          this.generateSeriesData('阳性', [4, 6, 11, 18, 48, 70, 231, 46, 55, 18, 10, 7], 0)
        ]
      }
    }
  },
  mounted() {
    // 在生命周期中挂载Echarts实例
    this.echartsInit()
  },
  methods: {
    // 初始化Echarts
    echartsInit() {
      echarts.init(document.getElementById('echarts1')).setOption(this.option)
    },
    // X轴线配置
    axisLineConfig(color) {
      return {
        onZero: false,
        lineStyle: {
          color: color
        }
      }
    },
    // X轴指示器配置
    axisPointerConfig(color) {
      return {
        label: {
          formatter: function (params) {
            return 'Precipitation  ' + params.value + (params.seriesData.length ? '：' + params.seriesData[0].data : '')
          }
        }
      }
    },
    // 生成X轴数据
    generateXAxisData(startYear) {
      const months = Array.from({ length: 12 }, (_, i) => i + 1)
      return months.map(month => startYear + '-' + '12-' + month)
    },
    // 生成系列数据
    generateSeriesData(name, data, xAxisIndex) {
      return {
        name: name,
        type: 'line',
        xAxisIndex: xAxisIndex,
        smooth: true,
        emphasis: {
          focus: 'series'
        },
        data: data
      }
    }
  }
}
</script>

<style scoped>
</style>
