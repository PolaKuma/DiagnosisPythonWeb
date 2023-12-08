<template>
  <div class="staffFlow">
    <span class="tittle">人员流动记录信息表</span>
    <div class="replyBtn">
      <el-button size="big" icon="el-icon-edit" type="primary" @click="handleCreate">添加离职人员信息</el-button>
    </div>
    <el-table :data="staffFlowlist" style="width: 100%;" height="500">
      <!-- <el-table-column label="人员流动信息表" class="tittle"> -->
      <el-table-column type="expand">
        <template scope="props">
          <el-form label-position="left" inline class="demo-table-expand">
            <el-form-item label="姓名">
              <span>{{ props.row.name }}</span>
            </el-form-item>
            <el-form-item label="性别">
              <span>{{ props.row.sex }}</span>
            </el-form-item>
            <el-form-item label="学历">
              <span>{{ props.row.degree }}</span>
            </el-form-item>
            <el-form-item label="专业">
              <span>{{ props.row.major }}</span>
            </el-form-item>
            <el-form-item label="职称">
              <span>{{ props.row.profession }}</span>
            </el-form-item>
            <el-form-item label="科室">
              <span>{{ props.row.office }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="医生 ID" prop="id"></el-table-column>
      <el-table-column label="医生姓名" prop="name"></el-table-column>
      <el-table-column label="入职日期" prop="date"></el-table-column>
      <el-table-column label="离职日期" prop="leave"></el-table-column>
      <el-table-column label="离职原因" prop="reason"></el-table-column>
      <el-table-column label="操作" align="center" width="300">
        <template v-slot="{row}">
          <el-button type="danger" size="mini" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
      <!-- </el-table-column> -->
    </el-table>
    <el-dialog title="添加人员流动信息" :visible.sync="dialogFormVisible">
      <el-form class="small-space" :model="form" label-position="left" label-width="70px"
               style='width: 400px; padding-left:50px;'>
        <el-form-item label="姓名">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.sex">
            <el-radio label="男"></el-radio>
            <el-radio label="女"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学历">
          <el-input v-model="form.degree"></el-input>
        </el-form-item>
        <el-form-item label="专业">
          <el-input v-model="form.major"></el-input>
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="form.profession"></el-input>
        </el-form-item>
        <el-form-item label="科室">
          <el-input v-model="form.office"></el-input>
        </el-form-item>
        <el-form-item label="医生 ID">
          <el-input v-model="form.id"></el-input>
        </el-form-item>
        <el-form-item label="入职日期">
          <el-input v-model="form.date"></el-input>
        </el-form-item>
        <el-form-item label="离职时间">
          <el-input v-model="form.leave"></el-input>
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

export default {
  data() {
    return {
      dialogFormVisible: false,
      staffFlowlist: [],
      form: {
        name: '',
        sex: '',
        degree: '',
        major: '',
        position: '',
        profession: '',
        office: '',
        id: '',
        date: '',
        leave: '',
        reason: ''
      }
    };
  },
  methods: {
    handleDelete(row) {
      const index = this.staffFlowlist.indexOf(row);
      if (flow !== -1) {
        this.staffFlowlist.splice(flow, 1);
        this.$message.success('删除成功');
      }
    },
    // 导出信息表
    handleCreate() {
      this.dialogFormVisible = true;
      // this.formClear();
    },
    formClear() {
      this.form = {
        name: '',
        sex: '',
        degree: '',
        major: '',
        position: '',
        profession: '',
        office: '',
        id: '',
        date: '',
        leave: '',
        reason: ''
      };
    },
    handleCreateSubmit() {
      let vm = this;
      console.log('修改后的信息：', vm.form, vm.staffFlowlist);
      vm.staffFlowlist.push(vm.form);
      this.dialogFormVisible = false;
    }
  },
  created() {
    // Simulating API response with example data
    const exampleData = [
      {
        id: 1,
        name: 'John Doe',
        date: '2023-01-01',
        leave: '2023-02-01',
        reason: 'Personal reasons',
        sex: 'Male',
        degree: 'PhD',
        major: 'Computer Science',
        profession: 'Senior Developer',
        office: 'Development',
      },
      {
        id: 2,
        name: 'Jane Smith',
        date: '2023-02-01',
        leave: '2023-03-01',
        reason: 'Relocation',
        sex: 'Female',
        degree: 'Masters',
        major: 'Business Administration',
        profession: 'Manager',
        office: 'Management',
      }
      // Add more dummy data as needed
    ];

    // Set the example data to staffFlowlist
    this.staffFlowlist = exampleData;
  },
};
</script>

<style scoped>
</style>
