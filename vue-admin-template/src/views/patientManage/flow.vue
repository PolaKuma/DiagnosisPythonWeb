<template>
  <div class="staffFlow">
    <div class="search">
      <el-input style="width: 200px;" placeholder="医生ID" v-model="searchName"></el-input>
      <el-button type="primary" icon="el-icon-search" @click="onState">搜索</el-button>
      <el-button type="primary" icon="" @click="getAll">显示全部</el-button>
    </div>
    <div class="replyBtn">
      <el-button v-if="usertype===1" size="big" icon="el-icon-edit" type="primary" @click="handleCreate">添加离职人员信息</el-button>
    </div>
    <el-table v-loading="loading" :data="tableData" :header-cell-style="{background:'#f5f7fa',color:'#606266'}" style="width: 100%;" height="400">
      <el-table-column type="expand">
        <template slot-scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="离职原因">
              <span>{{ props.row.reason }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="医生ID" prop="doctor_id"></el-table-column>
      <el-table-column label="医生姓名" prop="realname"></el-table-column>
      <el-table-column label="入职日期" prop="hiredate"></el-table-column>
      <el-table-column label="离职日期" prop="resigndate"></el-table-column>
      <el-table-column label="操作" align="center" width="300">
        <template v-slot="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
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
      @current-change="getFlowList"
      @size-change="handleSizeChange"
    />

    <el-dialog title="添加人员流动信息" :visible.sync="dialogFormVisible">
      <el-form class="small-space" :model="form" label-position="left" label-width="70px" style='width: 400px; padding-left:50px;'>
        <el-form-item label="医生ID">
          <el-input v-model="form.doctor_id"></el-input>
        </el-form-item>
        <el-form-item label="医生姓名">
          <el-input v-model="form.realname"></el-input>
        </el-form-item>
        <el-form-item label="入职日期">
          <el-input v-model="form.hiredate"></el-input>
        </el-form-item>
        <el-form-item label="离职原因">
          <el-input v-model="form.reason"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCreateSubmit">确 定</el-button>
        <el-button type="primary" @click="formClear">重置</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">

import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'usertype'
    ])
  },
  data() {
    return {
      tableData: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      dialogFormVisible: false,
      searchName: '',
      staffFlowlist: [],
      form: {
        doctor_id: '',
        realname: '',
        hiredate: '',
        reason: ''
      }
    }
  },
  mounted() {
    this.getFlowList(1)
  },
  methods: {
    async getFlowList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const { pageNum, pageSize } = this
      var search = this.searchName
      if (search === '') {
        search = 'None'
      }
      console.log(search)
      const res = await this.$API.flow.findFlow(pageNum, pageSize, search)
      if (res.code === 200) {
        this.tableData = res.msg
        this.total = res.total
        this.loading = false
      }
    },
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getFlowList()
    },
    handleDelete(row) {
      this.$confirm(`你确定删除 ${row.realname} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        const result = await this.$API.flow.delFlow(row.id)
        if (result.code === 200) {
          this.$notify({ type: 'success', message: '删除成功!' }, await this.getFlowList(this.tableData.length > 1 ? this.pageNum : this.pageNum - 1)
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
    // 导出信息表
    handleCreate() {
      this.dialogFormVisible = true
      this.formClear()
    },
    getAll() {
      this.searchName = ''
      this.getFlowList(1)
    },
    onState() {
      this.getFlowList(1)
    },
    formClear() {
      this.form = {
        doctor_id: '',
        realname: '',
        hiredate: '',
        reason: ''
      }
    },
    async handleCreateSubmit() {
      const res = await this.$API.flow.addFlow(this.form)
      if (res.code === 200) {
        // 关闭表单
        this.dialogFormVisible = false
        // 消息提示
        this.$message({
          message: '添加成功!',
          type: 'success'
        }, await this.getFlowList(this.form.id ? this.pageNum : 1))
      }
    }
  }
}
</script>
<style>
.staffFlow {
  width: 1160px;
  height: 500px;
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
