<template>
  <div class="percentage"></div>
</template>
<script>
export default {
  name: 'Percentage',
  props: {
    containerId: String,
    option: {}
  },
  data() {
    return {
      option1: {
        color: '#516c72',
        series: [{
          type: 'gauge',
          startAngle: 90,
          endAngle: -270,
          pointer: {
            show: false
          },
          progress: {
            show: true,
            overlap: false,
            roundCap: true,
            clip: false,
          },
          axisLine: {
            lineStyle: {
              color: [[1, '#464646']],
              width: 10,
            }
          },
          splitLine: {
            show: false,
            distance: 0,
            length: 10
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            show: false,
            distance: 50,
            backgroundColor: 'red'
          },
          data: [{
            value: 20,
            detail: {
              offsetCenter: ['0%', '0%']
            }
          },
          ],
          title: {
            fontSize: 14
          },
          detail: {
            width: 50,
            height: 14,
            fontSize: 14,
            color: 'auto',
            formatter: '{value}%'
          }
        }]
      },
    }
  },
  methods: {
    initChart(newOption) {
      if (newOption.series) {
        this.option1.series[0].data[0].value = newOption.series[0].data[0].value;
        this.option1.series[0].detail.formatter = newOption.series[0].detail.formatter;
        if (newOption.color) {
          this.option1.color = newOption.color
        }
      }
      let myChart = this.$echarts.init(
        document.getElementById(this.containerId)
      );
      //  console.log('this.option1',this.option1)
      myChart.setOption(this.option1);
    },
  }
}
</script>
<style scoped>
.percentage {
  width: 100%;
  height: 100%;
}
</style>
