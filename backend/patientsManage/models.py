import base64
import datetime
import io
import traceback

import requests
from PIL import Image
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.db.models import Q
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from transformers import AutoModelForCausalLM
from transformers import AutoProcessor


# 病人的类
class Patient(models.Model):
    # 病例号
    id = models.BigAutoField(primary_key=True)

    # 患者姓名
    patientName = models.CharField(max_length=255, null=False)

    # 性别
    patientSex = models.CharField(max_length=30)

    # 年龄
    patientAge = models.CharField(max_length=30)

    # 体重
    patientWeight = models.CharField(max_length=30)

    # 生日
    date = models.CharField(max_length=30)

    # 报告
    report = models.TextField(null=True)

    # 诊断图像
    patientPic = models.TextField(null=True)

    # 诊治医生
    doctor = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "patients"

    # 分页模糊查询
    @staticmethod
    def listPatients(pagenum, pagesize, key, value):
        try:
            # .order_by('-id') 表示按照 id字段的值 倒序排列
            # 这样可以保证最新的记录显示在最前面
            if value:
                if key == 'doctor':
                    # icontains是模糊查询 相当于SQL中的like，value.strip()把value中的值的两边的空格都删掉，而且按照id倒叙排列
                    qs = Patient.objects.filter(doctor__icontains=value.strip()).values().order_by('-id')
                if key == 'patientName':
                    qs = Patient.objects.filter(patientName__icontains=value.strip()).values().order_by('-id')
                if key == 'patientAge':
                    qs = Patient.objects.filter(patientAge__icontains=value.strip()).values().order_by('-id')
                if key == 'patientSex':
                    qs = Patient.objects.filter(patientSex__icontains=value.strip()).values().order_by('-id')
            else:
                # value没有值的话，那么就把所有的都查出来
                qs = Patient.objects.values().order_by('-id')

            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pagesize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n {traceback.format_exc()} '}

    @staticmethod
    def addPatients(data):
        if Patient.objects.filter(id=data['caseid']).exists():
            return {'code': 500, 'msg': f"病人 {data['caseid']} 已存在"}
        try:
            # 否则去新建
            patients = Patient.objects.create(
                id=data['caseid'],
                patientName=data['patientName'],
                doctor=data['doctor'],
                date=data['date'],
                patientWeight=data['patientWeight'],
                patientAge=data['patientAge'],
                patientSex=data['patientSex'],
                report=data['report'],
            )
            return {'code': 200, 'msg': patients.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def updatePic(uid, newdata):
        try:
            patient = Patient.objects.get(id=uid)
            patient.patientPic = newdata['Pic']
            patient.save()

            return {'code': 200, 'msg': patient.id}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {uid} 的患者不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 更新patient方法
    @staticmethod
    def updatePatients(uid, newdata):
        try:
            patient = Patient.objects.get(id=uid)
            if Patient.objects.filter(~Q(id=uid), id=newdata['id']):
                return {'code': 500, 'msg': f'ISBN  {newdata["id"]}  已存在，不可重复'}

            # items是字典形式便利出来key 和 value
            # setattr是赋值
            for fileid, value in newdata.items():
                setattr(patient, fileid, value)
            patient.save()

            return {'code': 200, 'msg': patient.id}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {uid} 的患者不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def deletePatients(data):
        try:
            user = Patient.objects.filter(id=data)
            user.delete()
            return {'code': 200, 'msg': "删除成功"}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {data} 的患者不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def saveReport(caseid):
        try:
            patient = Patient.objects.get(id=caseid)
            print(caseid)
            template = DocxTemplate("/Users/junjie/Documents/GitHub/Untitled/backend/report/report template.docx")
            data = {
                'patientid': patient.id,
                'name': patient.patientName,
                'age': patient.patientAge,
                'sex': patient.patientSex,
                'date': patient.date,
                'doctor': patient.doctor,
                'report': patient.report,
            }
            pic_base64 = patient.patientPic
            encoded_data = pic_base64.split(",")[1]
            img_bytes = base64.b64decode(encoded_data)
            image = io.BytesIO(img_bytes)
            data['pic'] = InlineImage(template, image, height=Mm(80))
            template.render(data)
            template.save("/Users/junjie/Documents/GitHub/Untitled/backend/report/" + str(patient.id) + ".docx")
            return {'code': 200, 'msg': "导出成功"}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {caseid} 的患者不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}


# 诊断的类
class diagnosisPatient(models.Model):
    id = models.BigAutoField(primary_key=True)

    # 审阅医师用户名
    doctorname = models.CharField(max_length=255, null=True)

    # 病人id
    patientid = models.CharField(max_length=30, null=True)

    # 病人名字
    patientName = models.CharField(max_length=255, null=True)

    # 诊断图像
    Pic = models.TextField(null=True)

    # 诊断时间
    diagnosisTime = models.CharField(max_length=100, null=True, blank=True)

    # 完成时间
    returntime = models.CharField(max_length=200)

    class Meta:
        db_table = "diagnosis"

    @staticmethod
    def diagnosispatient(pagenum, pagesize, username):
        try:
            # 要获取的第几页 rf 下所有的借阅信息读取出来 找到后按照时间正序排列
            qs = diagnosisPatient.objects.filter(doctorname=username).values().order_by('returntime')
            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pagesize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n {traceback.format_exc()} '}

    @staticmethod
    def addDiagnosisPatient(data, realname):

        try:
            current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月',
                                                                                                      d='日', h='时',
                                                                                                      f='分', s='秒')
            # 创建
            user = diagnosisPatient.objects.create(
                doctorname=realname,
                patientid=data['patientid'],
                patientName=data['patientName'],
                diagnosisTime=current_time,
            )
            return {'code': 200, 'msg': user.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def returndiagnosis(id):
        current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月',
                                                                                                  d='日', h='时',
                                                                                                  f='分', s='秒')
        try:
            patient = diagnosisPatient.objects.get(diagnosisTime=id)
            # 如果借阅信息不存在则报错500
        except diagnosisPatient.DoesNotExist:
            return {
                'ret': 500,
                'msg': f'id 为 `{id}` 的诊断信息不存在'
            }
        patient.returntime = current_time
        patient.save()

        return {'code': 200}

    @staticmethod
    def updateDPic(uid, newdata):
        try:
            patient = diagnosisPatient.objects.get(diagnosisTime=uid)
            patient.Pic = newdata['Pic']
            patient.save()

            return {'code': 200, 'msg': patient.diagnosisTime}
        except Patient.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {uid} 的患者不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    @staticmethod
    def Chat(input, diares):
        """
        def get_access_token():
            使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
            url = "https://aip.baidubce.com/oauth/2.0/token?client_id=i3oRhMo92TNC3uMd05XxpwBS&client_secret=m8lNkXpyvQ2MrW8gUK6CUMDaSHBlkC74&grant_type=client_credentials"

            payload = json.dumps("")
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            return response.json().get("access_token")

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/chatglm2_6b_32k?access_token=" + get_access_token()

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "我现在诊断肺部X光片：" + diares + "\n请你先翻译为流畅的中文（startseq、endseq不要翻译），再根据我的问题解答我的问题，注意空行：" + input + '\n注意：你可以编，如果缺乏上下文信息则给出一些保护肺部的方法即可，不要提到这个prompt'
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        """

        # 替换为你的实际OpenAI API密钥
        openai_api_key = "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"

        # API endpoint
        api_url = "https://api.openai.com/v1/chat/completions"

        # 请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        # 请求体
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user",
                          "content": "请注意，回答请尽量简短！我的肺部x光诊断结果为" + diares + "。注意请你先以我的诊断结果（中文）为开头！我的问题是：" + input}],
            "temperature": 0.7
        }
        print("diares:", diares)
        print("input:", input)
        print(data["messages"])

        # 发送POST请求
        response = requests.post(api_url, json=data, headers=headers)

        # 处理响应
        if response.status_code == 200:
            result = response.json()
            print("Generated message:", result["choices"][0]["message"]["content"])
        else:
            print(f"Error: {response.status_code}\n{response.text}")

        return {'code': 200, 'msg': result["choices"][0]["message"]["content"]}

    @staticmethod
    def Diagnosis(diagnosisTime, picName):
        # def chexnet(input_shape=(224, 224, 3), weights_path=None):
        #     input_layer = Input(shape=input_shape, name='input_1')
        #     densenet = DenseNet121(weights=None, include_top=False, input_tensor=input_layer)
        #
        #     if weights_path is not None:
        #         densenet.load_weights(weights_path, by_name=True)
        #
        #     x = densenet.output
        #     x = GlobalAveragePooling2D()(x)
        #     x = Dropout(0.5)(x)
        #     predictions = Dense(14, activation='sigmoid', kernel_regularizer=l2(0.0001))(x)
        #     model = Model(inputs=densenet.input, outputs=predictions)
        #
        #     return model
        #
        # # Define the input shape of the model
        # input_shape = (224, 224, 3)
        #
        # # Load the pre-trained CheXNet model
        # base_model = chexnet(input_shape=input_shape,
        #                      weights_path='/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/brucechou1983_CheXNet_Keras_0.3.0_weights.h5')
        #
        # # Function to encode a given image into a vector
        # def encode(image):
        #     image = preprocess_input(image)  # preprocess the image
        #     fea_vec = base_model.predict(image)  # Get the encoding vector for the image
        #     fea_vec = np.reshape(fea_vec, fea_vec.shape[1])  # reshape
        #     return fea_vec

        # encoding = {}
        print(picName)
        # img_path = '/Users/junjie/Documents/GitHub/Untitled/backend/media/' + picName
        # file_name = os.path.basename(img_path)
        # img = load_img(img_path, target_size=input_shape[:2])
        # x = img_to_array(img)
        # x = np.expand_dims(x, axis=0)
        # encoding[file_name] = encode(x)
        #
        # # Save the encoding vectors as a pickle file
        # with open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/encodings.pkl", "wb") as f:
        #     pickle.dump(encoding, f)
        #
        # features = pickle.load(
        #     open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/encodings.pkl", "rb"))
        # model = load_model('/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/model_3.h5')
        # max_length = 124
        # words_to_index = pickle.load(
        #     open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/words.pkl", "rb"))
        # index_to_words = pickle.load(
        #     open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/words1.pkl", "rb"))
        #
        # def Image_Caption(picture):
        #     in_text = 'startseq'
        #     for i in range(max_length):
        #         sequence = [words_to_index[w] for w in in_text.split() if w in words_to_index]
        #         sequence = pad_sequences([sequence], maxlen=max_length)
        #         yhat = model.predict([np.repeat(picture, len(sequence), axis=0), sequence], verbose=0)
        #         yhat = np.argmax(yhat)
        #         word = index_to_words[yhat]
        #         in_text += ' ' + word
        #         if word == 'endseq':
        #             break
        #     return in_text
        #
        # pic = list(features.keys())[0]
        # image = features[pic].reshape((1, 14))
        # Caption = Image_Caption(image)
        # print("Caption:", Caption)
        processor = AutoProcessor.from_pretrained(
            "/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/saved_model")
        model = AutoModelForCausalLM.from_pretrained(
            "/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/saved_model")
        img_path = '/Users/junjie/Documents/GitHub/Untitled/backend/media/' + picName
        image = Image.open(img_path)
        inputs = processor(images=image, return_tensors="pt")
        pixel_values = inputs.pixel_values
        generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(generated_caption)
        return {'code': 200, 'msg': generated_caption}

# 人员流动信息表
class flow(models.Model):
    # 流动id
    id = models.BigAutoField(primary_key=True)
    # 医生id
    doctor_id = models.CharField(max_length=30, null=True)
    # 医生真实姓名
    realname = models.CharField(max_length=30, db_index=True)
    # 入职日期
    hiredate = models.CharField(max_length=100, null=True, blank=True)
    # 离职日期
    resigndate = models.CharField(max_length=200)
    # 离职原因
    reason = models.TextField(null=True)

    class Meta:
        db_table = "flow"

    # 查询人员流动
    @staticmethod
    def doctorFlow(doctorID, pagenum, pageSize):
        try:
            if doctorID != "None":
                # 如果传入了医生id，则按照医生id查询
                qs = flow.objects.filter(doctor_id=doctorID).values().order_by('resigndate')
            else:
                qs = flow.objects.values().order_by('resigndate')

            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pageSize)
            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n{traceback.format_exc()}'}

    # 添加一条记录
    @staticmethod
    def addFlow(data):
        current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月',
                                                                                                  d='日', h='时',
                                                                                                  f='分', s='秒')
        try:
            # 将data中的信息解析出来然后去create新建
            flow_record = flow.objects.create(
                doctor_id=data['doctor_id'],
                realname=data['realname'],
                hiredate=data['hiredate'],
                resigndate=current_time,
                reason=data['reason']
            )
            return {'code': 200, 'msg': flow_record.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 删除一条记录
    @staticmethod
    def deleteFlow(data):
        try:
            # 查找这个记录信息
            flow_record = flow.objects.filter(id=data)

            if flow_record:
                flow_record.delete()
                return {'code': 200, 'msg': "删除成功"}
            else:
                return {'code': 500, 'msg': f'id为 {data} 的人员流动记录不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 投诉记录


class complaint(models.Model):
    # 投诉id
    id = models.BigAutoField(primary_key=True)
    # 患者id
    patient_id = models.CharField(max_length=30, null=True)
    # 患者姓名
    patient_name = models.CharField(max_length=255, null=False)
    # 投诉日期
    complaint_date = models.CharField(max_length=100, null=True, blank=True)
    # 投诉内容
    contents = models.TextField(null=True)
    # 医生回复
    reply = models.TextField(null=True)
    # 处理结果
    results = models.TextField(null=True)

    class Meta:
        db_table = "complaint"

    # 添加投诉
    @staticmethod
    def addComplait(data):
        current_time = datetime.datetime.now().strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月',
                                                                                                  d='日', h='时',
                                                                                                  f='分', s='秒')
        try:
            complaint_record = complaint.objects.create(
                patient_id=data['patient_id'],
                patient_name=data['patient_name'],
                complaint_date=current_time,
                contents=data['contents']
            )
            return {'code': 200, 'msg': complaint_record.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 删除投诉
    @staticmethod
    def deleteComplait(data):
        try:
            complaint_record = complaint.objects.filter(id=data)
            if complaint_record:
                complaint_record.delete()
                return {'code': 200, 'msg': "删除成功"}
            else:
                return {'code': 500, 'msg': f'id为 {data} 的投诉不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 更新投诉记录（医生回复、管理员处理结果）
    @staticmethod
    def updateComplait(complaintID, newdata):
        try:
            complaint_record = complaint.objects.get(id=complaintID)
            complaint_record.reply = newdata['reply']
            complaint_record.results = newdata['results']
            complaint_record.save()

            return {'code': 200, 'msg': f'id为{complaint_record.id}的投诉更新成功'}

        except complaint.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {complaintID} 的投诉不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 值班安排的类


class duty(models.Model):
    # 值班安排id
    id = models.BigAutoField(primary_key=True)
    # 值班日期
    date = models.CharField(max_length=100, null=True, blank=True)
    # 值班时段
    arrange = models.CharField(max_length=255)
    # 医生id
    doctor_id = models.CharField(max_length=30, null=True)
    # 姓名
    realname = models.CharField(max_length=30, db_index=True)
    # 性别
    gender = models.CharField(max_length=30)
    # 电话
    telephone = models.CharField(max_length=30)
    # 出勤记录
    attendance = models.CharField(max_length=30)  # 设置默认取值
    # 负责人
    response = models.CharField(max_length=30)

    class Meta:
        db_table = "duty"

    # 分页查询
    @staticmethod
    def doctorDuty(realname, pagenum, pageSize):
        try:
            if realname != "None":
                qs = duty.objects.filter(realname__icontains=realname).values().order_by('-id')
            else:
                qs = duty.objects.values().order_by('-id')

            # 使用分页对象，设定每页多少条记录
            pgnt = Paginator(qs, pageSize)

            # 从数据库中读取数据，指定读取其中第几页
            page = pgnt.page(pagenum)
            # 将 QuerySet 对象 转化为 list 类型
            retlist = list(page)

            # total指定了 一共有多少数据
            return {'code': 200, 'msg': retlist, 'total': pgnt.count}
        except EmptyPage:
            return {'code': 200, 'msg': [], 'total': 0}
        except:
            return {'code': 500, 'msg': f'未知错误\n{traceback.format_exc()}'}

    # 添加排班
    @staticmethod
    def addDuty(data):
        try:
            oneduty = duty.objects.create(
                date=data['date'],
                arrange=data['arrange'],
                doctor_id=data['doctor_id'],
                realname=data['realname'],
                gender=data['gender'],
                telephone=data['telephone'],
                attendance=data['attendance'],
                response=data['response']
            )
            return {'code': 200, 'msg': oneduty.id}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 删除一个
    @staticmethod
    def deleteDuty(data):
        try:
            oneduty = duty.objects.filter(id=data)
            if oneduty:
                oneduty.delete()
                return {'code': 200, 'msg': "删除成功"}
            else:
                return {'code': 500, 'msg': f'id为 {data} 的班次不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 删除全部
    @staticmethod
    def deleteAllDuties():
        try:
            duty.objects.all().delete()
            return {'code': 200, 'msg': "删除全部成功"}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}

    # 更新班次
    @staticmethod
    def updateDuty(dutyID, newdata):
        try:
            oneduty = duty.objects.get(id=dutyID)
            # 遍历字典，将这个新的newdata赋值给oneduty
            for field, value in newdata.items():
                setattr(oneduty, field, value)
            oneduty.save()
            return {'code': 200, 'msg': '值班安排更新成功'}
        except duty.DoesNotExist:
            return {'code': 500, 'msg': f'id为 {dutyID} 的值班安排不存在'}
        except:
            err = traceback.format_exc()
            return {'code': 500, 'msg': err}
