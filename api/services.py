import requests
import orjson

class PogodaSvHandler():
    def __init__(self) -> None:
        pass

    def get_impurities_data(self) -> dict:
        """
        Получает данные по загрязнению с сервера pogoda-sv.ru
        Возвращает словарь вида:
        {impurity_id:{
            'fullname': , 'unit': ,
            'concentration_limit': , 'value': , 'factor':
        }}
        factor - это данные по единицам ПДК, полученным с 
        pogoda-sv
        """
        url = 'http://pogoda-sv.ru/pollcenter/airdata/api/get_station_meas_last_list?station=11'
        response = requests.get(url)
        response_dict = orjson.loads(response.content)
        try:
            result = self._decode_response_pogodasv(response_dict)
        except KeyError as err:
            print('Something wrong/changed in response from pogoda-sv: ', err)
            return None
        # print(response_dict)
        return result

    @staticmethod
    def _decode_response_pogodasv(impurity_dict: dict):
        result_dict = {}
        for imp_id, imp_info in impurity_dict['11']['meas_list'].items():
            result_dict[imp_id] = {
                'fullname': imp_info['fullname'],
                'unit': imp_info['unit'],
                'concentration_limit': imp_info['concentration_limit'],
                }
        for imp_id, imp_data in impurity_dict['11']['meas_last_list'].items():
            c_limit = result_dict[imp_id]['concentration_limit']
            if imp_data['factor']:
                result_dict[imp_id]['factor'] = round(imp_data['factor'], 2)*100
            else:
                result_dict[imp_id]['factor'] = 0
            if c_limit != 0:
                result_dict[imp_id]['unit'] = 'pdf_percent'
                result_dict[imp_id]['value'] = imp_data['value']*100 / c_limit
            else:
                result_dict[imp_id]['value'] = imp_data['value']
        return result_dict
        


pogoda_handler = PogodaSvHandler()      

if __name__ == '__main__':
    
    a = pogoda_handler.get_impurities_data()
    print(a)
    