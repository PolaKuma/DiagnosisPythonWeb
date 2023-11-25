<template>
  <div>
    <el-button type="primary" v-if="usertype===1" @click="AddForm">增加人员</el-button>
    <el-table :data="tableData" v-loading="loading" style="width: 100%">
      <el-table-column type="index" label="序号" align="center" width="70"/>
      <el-table-column prop="doctorno" label="工号" align="center" width="180"/>
      <el-table-column prop="username" label="登录名" align="center" width="180"/>
      <el-table-column prop="realname" label="姓名" align="center" width="180"/>
      <el-table-column prop="usertype" label="职称" align="center" width="180">
        <template v-slot="{row}">
          <el-tag :type="row.usertype === 1 ? 'dark' : '' " effect="danger">
            {{ row.usertype === 1 ? "主任" : "医师" }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="date_joined" label="日期" align="center"/>
      <el-table-column label="操作" align="center" width="300">
        <template v-slot="{row}">
          <el-button v-if="usertype===1" type="primary" @click="showForm(row)" size="mini">编辑</el-button>
          <el-button v-if="usertype===1" type="danger" @click="deleted(row)" size="mini">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      style="margin-top: 20px;text-align: center"
      :current-page="pageNum"
      :page-size="pageSize"
      :total="total"
      :pager-count="5"
      :page-sizes="[5,15,30]"
      layout="prev,pager,next,jumper,->,sizes,total"
      @current-change="getUserList"
      @size-change="handleSizeChange"
    />

    <el-dialog :title="form.id ? '修改用户':'新增用户'" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="工号" :label-width="formLabelWidth">
          <el-input v-model="form.doctorno" autocomplete="off" style="width: 300px;"></el-input>
        </el-form-item>
        <el-form-item label="姓名" :label-width="formLabelWidth">
          <el-input v-model="form.realname" autocomplete="off" style="width: 300px;"></el-input>
        </el-form-item>
        <el-form-item label="登录名" :label-width="formLabelWidth">
          <el-input v-model="form.username" autocomplete="off" style="width: 300px;"></el-input>
        </el-form-item>
        <el-form-item label="登陆密码" :label-width="formLabelWidth">
          <el-input v-model="password" type="password" placeholder="默认密码：123456" autocomplete="off"
                    style="width: 300px;"></el-input>
        </el-form-item>
        <el-form-item label="权限" :label-width="formLabelWidth">
          <el-select v-model="form.usertype" placeholder="请选择权限">
            <el-option label="主任" value="1"></el-option>
            <el-option label="医师" value="2"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="onForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: 'user',
  computed: {
    ...mapGetters([
      'usertype'
    ])
  },
  data() {
    return {
      tableData: [],
      dialogFormVisible: false,
      infoDialogVisible: false,
      form: {
        username: '',
        usertype: '',
        realname: '',
        doctorno: ''
      },
      password: '',
      formLabelWidth: '120px',
      pageSize: 5,
      pageNum: 1,
      total: 0,
      loading: false
    }
  },
  mounted() {
    this.getUserList()
  },
  methods: {
    async getUserList(pager = 1) {
      this.loading = true
      this.pageNum = pager
      const {pageNum, pageSize} = this // 发送请求时候需要带参数
      const res = await this.$API.user.reqUser(pageNum, pageSize)
      if (res.code === 200) {
        this.tableData = res.msg
        this.total = res.total
        this.loading = false
      }
    },
    showForm(row) {
      this.dialogFormVisible = true
      this.form = {
        id: row.id,
        username: row.username,
        usertype: row.usertype.toString(),
        realname: row.realname,
        doctorno: row.doctorno
      }
      this.password = ''
    },
    async onForm() {
      const res = await this.$API.user.reqSaveAndUpdateUser(this.form, this.password)

      if (res.code === 200) {
        // 关闭表单
        this.dialogFormVisible = false
        // 消息提示
        this.$message({
          message: '添加成功!',
          type: 'success'
        });
        await this.getUserList(this.form.id ? this.pageNum : 1)
      }
    },
    deleted(row) {
      this.$confirm(`你确定删除 ${row.username} 吗?`, '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const result = await this.$API.user.delUser(row.id)
        if (result.code === 200) {
          this.$notify({
              type: 'success',
              message: '删除成功!'
            },
            await this.getUserList(this.tableData.length > 1 ? this.pageNum : this.pageNum - 1)
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
    handleSizeChange(limit) {
      this.pageSize = limit
      this.getUserList()
    },
    AddForm() {
      this.dialogFormVisible = true
      this.form = {
        username: '',
        password: '',
        usertype: '',
        realname: '',
        desc: '',
        studentno: ''
      }
    }
  }
}
</script>

<style scoped>

</style>
