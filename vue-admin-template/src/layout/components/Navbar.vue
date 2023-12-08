<template>
  <div class="navbar">
    <hamburger :is-active="sidebar.opened" class="hamburger-container" @toggleClick="toggleSideBar"/>

    <breadcrumb class="breadcrumb-container"/>

    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <img src="./ava.jpeg" class="user-avatar">
          <i class="el-icon-caret-bottom"/>
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/helloworld">
            <el-dropdown-item>
              Home
            </el-dropdown-item>
          </router-link>
          <a target="_blank" @click="dialogFormVisible = true">
            <el-dropdown-item>修改密码</el-dropdown-item>
          </a>
          <a target="_blank" @click="dialogFormVisible_off = true">
            <el-dropdown-item>申请离职</el-dropdown-item>
          </a>
          <el-dropdown-item divided @click.native="logout">
            <span style="display:block;">退出登录</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
    <el-dialog title="修改密码" width="50%" :visible.sync="dialogFormVisible">
      <el-form :model="form">
        <el-form-item label="用户名" :label-width="formLabelWidth">
          <a> {{ name }}</a>
        </el-form-item>
        <el-form-item label="密码" :label-width="formLabelWidth">
          <el-input v-model="form.password" show-password autocomplete="off" style="width: 300px;"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" :label-width="formLabelWidth">
          <el-input v-model="form.reqpassword" show-password autocomplete="off" style="width: 300px;"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="updatepassword">确 定</el-button>
      </div>
    </el-dialog>
    <!-- el-dialog 包含离职表单 -->
    <div id="pdfDom">
      <el-dialog :visible.sync="dialogFormVisible_off" title="申请离职">
        <el-form :model="ruleForm" label-width="100px" class="demo-ruleForm" ref="ruleForm">
          <!-- 员工基本信息 -->
          <h2 style="margin-bottom:20px;">员工基本信息:</h2>
          <div>
            <el-form-item label="姓名" prop="name">
              <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
            <el-form-item label="班组/科室" prop="department">
              <el-input v-model="ruleForm.department"></el-input>
            </el-form-item>
            <el-form-item label="职务/岗位" prop="jobs">
              <el-input v-model="ruleForm.jobs"></el-input>
            </el-form-item>
          </div>
          <div>
            <el-form-item label="入职日期" prop="hiredate" class="demonstration">
              <el-date-picker v-model="ruleForm.hiredate" type="date" placeholder="选择日期"
                              :picker-options="pickerOptions"></el-date-picker>
            </el-form-item>
            <el-form-item label="离职日期" prop="leaveDate">
              <el-date-picker v-model="ruleForm.leaveDate" type="date" placeholder="选择日期"
                              :picker-options="pickerOptions"></el-date-picker>
            </el-form-item>
            <el-form-item label="学历" prop="education">
              <el-input v-model="ruleForm.education"></el-input>
            </el-form-item>
          </div>

          <!-- 离职类别 -->
          <h2 style="margin-bottom:20px;">离职类别</h2>
          <div>
            <el-checkbox-group v-model="ruleForm.category" :min="1" :max="1">
              <el-checkbox label="辞职"></el-checkbox>
              <el-checkbox label="辞退"></el-checkbox>
              <el-checkbox label="除名"></el-checkbox>
              <el-checkbox label="自动离职"></el-checkbox>
              <el-checkbox label="合同到期"></el-checkbox>
              <el-checkbox label="其他"></el-checkbox>
            </el-checkbox-group>
          </div>

          <!-- 离职情况 -->
          <h2 style="margin-top:20px; margin-bottom:20px;">离职情况</h2>
          <div>
            <el-form-item label="申请离职日期" prop="applicationTime" class="demonstration">
              <el-date-picker v-model="ruleForm.applicationTime" type="date" placeholder="选择日期"
                              :picker-options="pickerOptions"></el-date-picker>
            </el-form-item>
            <el-form-item label="核准离职日期" prop="approvedTime">
              <el-date-picker v-model="ruleForm.approvedTime" type="date" placeholder="选择日期"
                              :picker-options="pickerOptions"></el-date-picker>
            </el-form-item>
            <el-form-item label="离职原因" prop="reason">
              <el-input v-model="ruleForm.reason"></el-input>
            </el-form-item>
          </div>
          <span style="margin-bottom:20px;">
          本人自愿与安逸医院解除劳动关系，自签字之日起任何行为与安逸医院无关，并自我承当责任。
        </span>

          <!-- 审批情况 -->
          <div>
            <h2 style="margin:20px 0px;">审批情况:</h2>
            <el-form-item label="部门主管签字" prop="departmentManager">
              <el-input v-model="ruleForm.departmentManager"></el-input>
            </el-form-item>
            <el-form-item label="院长签字" prop="director">
              <el-input v-model="ruleForm.director"></el-input>
            </el-form-item>
            <span>注:1.本表一人事管理审批权限逐级核准</span>
          </div>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button type="primary" @click="onSubmit">导出</el-button>
          <el-button @click="offReset">重置</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'
import html2Canvas from 'html2canvas'
import jsPDF from 'jspdf'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar',
      'name'
    ])
  },
  data() {
    const validatereqpassword = (rule, value, callback) => {
      if (value !== password) {
        callback(new Error('两次密码不一样'))
      } else {
        callback()
      }
    }
    return {
      dialogFormVisible_off: false,
      htmlTitle: '员工离职表',
      ruleForm: {
        name: '',
        department: '',
        jobs: '',
        hiredate: '',
        leaveDate: '',
        education: '',
        category: [],
        applicationTime: '',
        approvedTime: '',
        reason: '',
        departmentManager: '',
        director: ''
      },
      pickerOptions: {
        // 你的日期选择器配置选项
      },
      form: {
        password: '',
        reqpassword: ''
      },
      formLabelWidth: '120px',
      dialogFormVisible: false
    }
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    },
    async updatepassword() {
      const req = await this.$API.user.reqPasswordUP(this.form.reqpassword)
      if (req.code === 200) {
        this.$notify({
          type: 'success',
          message: '更改密码成功，请重新登录'
        })
        await this.logout()
      }
    },
    onSubmit() {
      var title = this.htmlTitle
      html2Canvas(document.querySelector('#pdfDom'), {
        allowTaint: true,
        taintTest: false,
        useCORS: true,
        y: 72, // 对Y轴进行裁切
        // width:1200,
        // height:5000,
        dpi: window.devicePixelRatio * 4,
        scale: 4 //按比例增加分辨率
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
      this.dialogFormVisible_off = false;
    },
    offReset() {
      // 重置表单
      this.$refs.ruleForm.resetFields();
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, .08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background .3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, .025)
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: rgba(0, 0, 0, .025)
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}
</style>
