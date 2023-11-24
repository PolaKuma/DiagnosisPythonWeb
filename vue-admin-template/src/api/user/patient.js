import request from "@/utils/request";

export const reqPatients = (pageNum, pageSize, key, value) => request({
  url: `api/patients`,
  method: 'post',
  data: {'action': 'listPatients', 'pageNum': pageNum, 'pageSize': pageSize, 'key': key, 'value': value}
})

export const reqSaveAndUpdatePatients = (patient) => {

  if (patient.id) {
    return request({url: `api/patients`, method: 'put', data: {"action": "updatePatients", "newdata": patient}})
  } else {
    return request({url: `api/patients`, method: 'post', data: {"action": "addPatients", "data": patient}})
  }
}
export const addPic = (Picdata) => {
  request({url: `api/patients`, method: 'post', data: {"action": "addPic", "data": Picdata}})
}
export const delPatients = (id) => request({url: `api/patients`, method: 'delete', data: {"action": "deletePatients", "id": id}})

// 借阅管理的API

export const reqDiagnosis = (pageNum, pageSize) => request({
  url: `api/diagnosis`,
  method: 'post',
  data: {'action': 'readlist', 'pageNum': pageNum, 'pageSize': pageSize}
})

export const diagnosisPatient = (data) => request({url: `api/diagnosis`, method: 'post', data: {'action': 'readbook', 'data': data}})

export const returnBook = (id) => request({url: `api/diagnosis`, method: 'post', data: {'action': 'returnbook', 'data': id}})

export const addDPic = (Picdata) => {
  request({ url: `api/diagnosis`, method: 'post', data: {"action": "addPic", "data": Picdata }})
}

export const diagnosis = (Picdata) => {
  return request({ url: `api/diagnosis`, method: 'post', data: {"action": "Diagnosis", "data": Picdata }})
}

export const chat = (commit) => {
  return request({ url: `api/diagnosis`, method: 'post', data: {"action": "chat", "data": commit }})
}