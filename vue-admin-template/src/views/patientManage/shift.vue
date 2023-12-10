<template>
  <div class="shift">
    <div class="title">
    </div>
    <div class="search">
      <el-input style="width: 200px;" class="filter-item" placeholder="请输入姓名" v-model="searchName"></el-input>
      <el-button class="filter-item" type="primary" icon="el-icon-search" @click="handelSearch">搜索</el-button>
      <el-button type="primary" icon="" @click="getAll">显示全部</el-button>
      <el-button v-if="usertype===1" class="filter-item" type="primary" @click="handelCreate" icon="el-icon-edit">添加</el-button>
      <el-button v-if="usertype===1" class="filter-item" type="primary" @click="handleDelAll" icon="el-icon-delete">清空</el-button>
      <el-button class="filter-item" type="primary" icon="el-icon-share" @click="handleDownload">导出</el-button>
    </div>

    <el-table id="pdf" :header-cell-style="{background:'#f5f7fa',color:'#606266'}" :data="table" border style="width: 100%"
              height="400">
      <el-table-column fixed="left" type="index" label="序号" align="center" width="70"/>
      <el-table-column prop="date" fixed label="日期" width="120"/>
      <el-table-column prop="arrange" label="时段" width="200"/>
      <el-table-column prop="doctor_id" label="医生ID" width="150"/>
      <el-table-column prop="realname" label="姓名" width="150"/>
      <el-table-column prop="gender" label="性别" width="150"/>
      <el-table-column prop="telephone" label="电话号码" width="150"/>
      <el-table-column prop="attendance" label="出勤情况" width="120"/>
      <el-table-column prop="response" label="负责人" width="120"/>
      <el-table-column align="center" label="操作" fixed="right" width="200px">
        <template v-slot="{row}">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      style="margin-top: 20px;text-align: center"
      :current-page="pageNum"
      :page-size="pageSize"
      :total="total"
      :pager-count="10"
      :page-sizes="[10,15,30]"
      layout="prev,pager,next,jumper,->,sizes,total"
      @current-change="getShiftList"
      @size-change="handleSizeChange"
    />
    <!-- 对话框 -->
    <el-dialog
      :title="form.id ? '修改值班信息':'新增值班信息'"
      :visible.sync="dialogFormVisible"
      width="50%"
      @close="resetForm"
    >
      <el-form :model="form" ref="formData" label-width="80px" style="margin-bottom: 20px;">
        <el-form-item label="日期">
          <el-date-picker v-model="form.date" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="时段">
          <el-select v-model="form.arrange" placeholder="选择时段">
            <el-option label="早班8:00-12:00" value="早班8:00-12:00"></el-option>
            <el-option label="午班12:00-18:00" value="午班12:00-18:00"></el-option>
            <el-option label="晚班18:00-24:00" value="晚班18:00-24:00"></el-option>
            <el-option label="夜班0:00-8:00" value="夜班0:00-8:00"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="医生ID">
          <el-input v-model="form.doctor_id" placeholder="请输入医生ID"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.realname" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话号码">
          <el-input v-model="form.telephone" placeholder="请输入电话号码"></el-input>
        </el-form-item>
        <el-form-item label="出勤情况">
          <el-select v-model="form.attendance" placeholder="选择出勤情况">
            <el-option label="迟到" value="迟到"></el-option>
            <el-option label="按时值班" value="按时值班"></el-option>
            <el-option label="请假" value="请假"></el-option>
            <el-option label="旷工" value="旷工"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="form.response" placeholder="请输入负责人"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCreateSubmit(form.id)">确 定</el-button>
        <el-button type="primary" @click="formClear">重置</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>

import html2Canvas from 'html2canvas'
import jsPDF from 'jspdf'
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'usertype'
    ])
  },
  data() {
    return {
      table: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      searchName: '',
      dialogFormVisible: false,
      editingRowIndex: -1,
      form: {
        date: '',
        arrange: '',
        doctor_id: '',
        realname: '',
        gender: '',
        telephone: '',
        attendance: '',
        response: ''
      }
    }
  },
  mounted() {
    this.getShiftList(1)
  },
  methods: {
    async getShiftList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const { pageNum, pageSize } = this
      var search = this.searchName
      if (search === '') {
        search = 'None'
      }
      const res = await this.$API.flow.findDuty(pageNum, pageSize, search)
      if (res.code === 200) {
        this.table = res.msg
        this.total = res.total
        this.loading = false
      }
    },
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getShiftList()
    },
    handleEdit(row) {
      this.form = {...row}
      this.dialogFormVisible = true
    },
    // 搜索
    handelSearch() {
      this.getShiftList(1)
    },
    handleDownload() {
      var title = '值班表'
      html2Canvas(document.querySelector('#pdf'), {
        allowTaint: true,
        taintTest: false,
        useCORS: true,
        y: 72, // 对Y轴进行裁切
        // width:1200,
        // height:5000,
        dpi: window.devicePixelRatio * 4,
        scale: 4
      }).then(function (canvas) {
        let contentWidth = canvas.width
        let contentHeight = canvas.height
        let pageHeight = contentWidth / 592.28 * 841.89
        let leftHeight = contentHeight
        let position = 0
        let imgWidth = 595.28
        let imgHeight = 592.28 / contentWidth * contentHeight
        let pageData = canvas.toDataURL('image/jpeg', 1.0)
        let PDF = new jsPDF('', 'pt', 'a4')
        if (leftHeight < pageHeight) {
          PDF.addImage(pageData, 'JPEG', 0, 0, imgWidth, imgHeight)
        } else {
          while (leftHeight > 0) {
            PDF.addImage(pageData, 'JPEG', 0, position, imgWidth, imgHeight)
            leftHeight -= pageHeight
            position -= 841.89
            if (leftHeight > 0) {
              PDF.addPage()
            }
          }
        }
        PDF.save(title + '.pdf')
      })
    },
    // 显示全部
    getAll() {
      this.searchName = ''
      this.getShiftList(1)
    },
    // 删除
    handleDelete(row) {
      this.$confirm(`你确定删除 ${row.realname} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.flow.delDuty(row.id)
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: '删除成功!'
            }, await this.getShiftList(this.table.length > 1 ? this.pageNum : this.pageNum - 1)
          )
        } else {
          this.$notify({
            type: 'warning',
            message: '删除失败,请联系系统运维!'
          })
        }
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 清空
    handleDelAll() {
      this.$confirm(`你确定清空值班记录吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.flow.delAllDuty()
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: '清空成功!'
            }, await this.getShiftList(this.table.length > 1 ? this.pageNum : this.pageNum - 1)
          )
        } else {
          this.$notify({
            type: 'warning',
            message: '删除失败,请联系系统运维!'
          })
        }
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    // 添加
    handelCreate() {
      this.dialogFormVisible = true
      this.formClear()
    },
    // 添加提交
    async handleCreateSubmit(id) {
      if (id) {
        const res = await this.$API.flow.update_Duty(this.form)
        if (res.code === 200) {
          // 关闭表单
          this.dialogFormVisible = false
          // 消息提示
          this.$message({
            message: '修改成功!',
            type: 'success'
          }, await this.getShiftList(this.form.id ? this.pageNum : 1))
        }
      } else {
        const res = await this.$API.flow.add_Duty(this.form)
        if (res.code === 200) {
          // 关闭表单
          this.dialogFormVisible = false
          // 消息提示
          this.$message({
            message: '添加成功!',
            type: 'success'
          }, await this.getShiftList(this.form.id ? this.pageNum : 1))
        }
      }
    },
    // 清空表单
    formClear() {
      this.form = {
        date: '',
        arrange: '',
        doctor_id: '',
        realname: '',
        gender: '',
        telephone: '',
        attendance: '',
        response: ''
      }
    },
    // 重置表单
    resetForm() {
      this.form = {
        date: '',
        arrange: '',
        doctor_id: '',
        realname: '',
        gender: '',
        telephone: '',
        attendance: '',
        response: ''
      }
      this.editingRowIndex = -1
    }
  }
}
</script>

<style>
.shift {
  height: 700px;
  width: 1160px;
  background-color: white;
  box-shadow: 0 15px 30px rgba(0, 0, 0, .3);
}

.search {
  padding: 30px;
  padding-bottom: 10px;
}

.el-button {
  margin-left: 10px;
  margin-bottom: 30px;
  border-radius: 10%;
  margin-left: 30px;
}
</style>
