import datetime
import json
import os
import pickle
import traceback

import numpy as np
import requests
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from django.db.models import Q
from keras.applications.densenet import DenseNet121
from keras.applications.densenet import preprocess_input
from keras.layers import Dropout
from keras.layers import Input, Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.regularizers import l2
from keras.utils import load_img, img_to_array


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
        def get_access_token():
            """
            使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
            """

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
        return {'code': 200, 'msg':data['result']}

    @staticmethod
    def Diagnosis(diagnosisTime, picName):
        def chexnet(input_shape=(224, 224, 3), weights_path=None):
            input_layer = Input(shape=input_shape, name='input_1')
            densenet = DenseNet121(weights=None, include_top=False, input_tensor=input_layer)

            if weights_path is not None:
                densenet.load_weights(weights_path, by_name=True)

            x = densenet.output
            x = GlobalAveragePooling2D()(x)
            x = Dropout(0.5)(x)
            predictions = Dense(14, activation='sigmoid', kernel_regularizer=l2(0.0001))(x)
            model = Model(inputs=densenet.input, outputs=predictions)

            return model

        # Define the input shape of the model
        input_shape = (224, 224, 3)

        # Load the pre-trained CheXNet model
        base_model = chexnet(input_shape=input_shape,
                             weights_path='/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/brucechou1983_CheXNet_Keras_0.3.0_weights.h5')

        # Function to encode a given image into a vector
        def encode(image):
            image = preprocess_input(image)  # preprocess the image
            fea_vec = base_model.predict(image)  # Get the encoding vector for the image
            fea_vec = np.reshape(fea_vec, fea_vec.shape[1])  # reshape
            return fea_vec

        encoding = {}
        print(picName)
        img_path = '/Users/junjie/Documents/GitHub/Untitled/backend/media/' + picName
        file_name = os.path.basename(img_path)
        img = load_img(img_path, target_size=input_shape[:2])
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        encoding[file_name] = encode(x)

        # Save the encoding vectors as a pickle file
        with open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/encodings.pkl", "wb") as f:
            pickle.dump(encoding, f)

        features = pickle.load(
            open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/encodings.pkl", "rb"))
        model = load_model('/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/model_3.h5')
        max_length = 124
        words_to_index = pickle.load(
            open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/words.pkl", "rb"))
        index_to_words = pickle.load(
            open("/Users/junjie/Documents/GitHub/Untitled/backend/patientsManage/words1.pkl", "rb"))

        def Image_Caption(picture):
            in_text = 'startseq'
            for i in range(max_length):
                sequence = [words_to_index[w] for w in in_text.split() if w in words_to_index]
                sequence = pad_sequences([sequence], maxlen=max_length)
                yhat = model.predict([np.repeat(picture, len(sequence), axis=0), sequence], verbose=0)
                yhat = np.argmax(yhat)
                word = index_to_words[yhat]
                in_text += ' ' + word
                if word == 'endseq':
                    break
            return in_text

        pic = list(features.keys())[0]
        image = features[pic].reshape((1, 14))
        Caption = Image_Caption(image)
        print("Caption:", Caption)
        return {'code': 200, 'msg': Caption}
