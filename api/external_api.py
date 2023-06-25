import httpx
import os
from api.schemas import User, Calendar, CourseList
from api.models import CourseDataModel
from api.utils import ZubronHelper
from pydantic import ValidationError


class Formatter:
    @staticmethod
    def get_data(params, service, token):
        return {
            'json': {
                'params': params,
                'appId': '3860928005924439',
                'methodName': 'invoke',
                'clientVersion': '1.0',
                'clientID': '2',
                'service': service,
                'token': token,
            },
        }

    @staticmethod
    def get_grades_data(user_info: User, course_data: CourseDataModel):
        return {
            'json': {
                'params': {
                    'roleId': 'student',
                    'studentId': user_info.userId,
                    'userId': user_info.userId,
                    'userData': {
                        'userBB': user_info.userNC,
                    },
                    'lang': 'es',
                    'careerId': user_info.careersList[0],
                    'courseData': course_data.dict(),
                    'courseNC': f'{course_data.courseId}_{course_data.section}',
                    'userNC': user_info.userNC,
                    'courseId': None,
                },
                'appId': '3860928005924439',
                'methodName': 'invoke',
                'clientVersion': '1.0',
                'clientID': '2',
                'service': 'gradesGetGradesByCourseClientV4',
                'token': user_info.token,
            },
        }


class ExternalApi:
    def __init__(self, username=None, password=None):
        self.base_url = "https://aiep.cl.api.mooestroviva.com/moofwd-rt/gateway.sjson"
        self.headers = {
            'accept-encoding': 'gzip',
            'connection': 'Keep-Alive',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'host': 'aiep.cl.api.mooestroviva.com',
            'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; CAM-L03 Build/HUAWEICAM-L03)',
        }
        self.username = username
        self.password = password

    async def call_service(self, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=self.headers, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                # Handle the error case
                return None


    async def get_user_info(self) -> User:
        try:
            token = ZubronHelper.get_encrypted_token()
            params = {
                'deviceId': '6e3d8b16b33c6e5e',
                'password': self.password,
                'os_version': '3.10.86-g25d9364',
                'username': self.username.split("@")[0],
                'model': 'CAM-L03',
                'lang': 'es',
            }

            data = Formatter.get_data(params, 'authLoginClientAlumniV54', token)

            response = await self.call_service(data)

            if response:
                login_response = response.get(
                    'response', {}).get('loginResponse', {})
                user_data = {
                    'userId': login_response.get('userId'),
                    'userNC': login_response.get('userNC'),
                    'careersList': [career['careerId'] for career in login_response.get('careersList', [])],
                    'campus': login_response.get('sede'),
                    'name': login_response.get('name'),
                    'token': ZubronHelper.get_encrypted_token(login_response.get('userNC'))
                }

                return User(**user_data)

        except ValidationError:
            return None

    async def get_schedule(self, user: User) -> Calendar:
        data = Formatter.get_data(
            user.to_params(), "scheduleGridClientV6", user.token)

        response = await self.call_service(data)


        if not response.get('error'):
            return response
        
        raise Exception(response.get('error').get('ErrorMessage'))



    async def get_courses(self, user: User) -> CourseList:
        data = Formatter.get_data(
                user.to_params(), "courseGetListClientV5", user.token)
        response = await self.call_service(data)

        if not response.get('error'):
            return response
        
        raise Exception(response.get('error').get('ErrorMessage'))



    async def get_grades(self, user: User, course_data: CourseDataModel):
        try:
            data = Formatter.get_grades_data(user, course_data)
            response = await self.call_service(data)
            
            if not response.get('error'):
                return response
            
            raise Exception(response.get('error').get('ErrorMessage'))

        except ValidationError:
            return None
