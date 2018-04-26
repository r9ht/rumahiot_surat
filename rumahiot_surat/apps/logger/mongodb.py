from pymongo import MongoClient

from rumahiot_surat.settings import RUMAHIOT_GUDANG_MONGO_HOST, \
    RUMAHIOT_GUDANG_MONGO_PASSWORD, \
    RUMAHIOT_GUDANG_MONGO_USERNAME, \
    RUMAHIOT_GUDANG_DATABASE, \
    RUMAHIOT_SURAT_DEVICE_NOTIFICATION_LOG_COLLECTION


class SuratMongoDB:

    # initiate the client
    def __init__(self):
        self.client = MongoClient(RUMAHIOT_GUDANG_MONGO_HOST,
                                  username=RUMAHIOT_GUDANG_MONGO_USERNAME,
                                  password=RUMAHIOT_GUDANG_MONGO_PASSWORD,
                                  )

    # Put data into specified database and collection
    # input parameter : database(string), collection(string), data(dictionary)
    # return : result(dict)
    def put_data(self, database, collection, data):
        db = self.client[database]
        col = db[collection]
        result = col.insert_one(data)
        return result

    # Put device notification log data
    # input parameter : data (dict)
    # return : result(dict)
    # data format :
    # data = {
    #     'user_uuid':  user uuid (string),
    #     'device_uuid': device uuid (string),
    #     'device_name': device name(string),
    #     'user_sensor_uuid': user sensor uuid (string),
    #     'user_sensor_name': user sensor name (string),
    #     'threshold_value': threshold value (float),
    #     'latest_value': latest sensor value (float),
    #     'time_reached': time reached (float, unix timestamp),
    #     'threshold_direction': 1 for above and -1 for below (string),
    #     'unit_symbol': unit symbol for sensor and threshold value (string),
    #     'notification_type': notifiation type , 0 for back to normal , 1 for over threshold (string),
    #     'sent': notification status 1 sent, 0 failed to sent (string),
    #     'viewed': notification viewed status (string)
    # }
    def put_device_notification_log(self, data):
        result = self.put_data(RUMAHIOT_GUDANG_DATABASE, RUMAHIOT_SURAT_DEVICE_NOTIFICATION_LOG_COLLECTION, data)
        return result

    # Get notification log using device_sensor_notification_log_uuid
    # input parameter : device_sensor_notification_log_uuid(string), viewed (string, 1 for viewed, 0 for unviewed notification)
    # output : result (dict)
    def get_notification_log_by_uuid(self, device_sensor_notification_log_uuid, viewed):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_SURAT_DEVICE_NOTIFICATION_LOG_COLLECTION]
        result = col.find_one({'device_sensor_notification_log_uuid': device_sensor_notification_log_uuid, 'viewed' : viewed})
        return result

    # Get notification log using device_sensor_notification_log_uuid
    # input parameter : device_sensor_notification_log_uuid(string), viewed (string, 1 for viewed, 0 for unviewed notification)
    # output : result (dict)
    def get_notification_log_by_user_uuid(self, user_uuid, viewed, direction):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_SURAT_DEVICE_NOTIFICATION_LOG_COLLECTION]
        result = col.find(
            {'user_uuid': user_uuid, 'viewed': viewed}).sort([("time_reached", direction)])
        return result

    # Update notification view status
    # input parameter : object_id (string), new_viewed_status (string)
    def update_notification_log_viewed_status(self, object_id, new_viewed_status):
        db = self.client[RUMAHIOT_GUDANG_DATABASE]
        col = db[RUMAHIOT_SURAT_DEVICE_NOTIFICATION_LOG_COLLECTION]
        col.update_one({'_id': object_id}, {'$set': {'viewed': new_viewed_status}})