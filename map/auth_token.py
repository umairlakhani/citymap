from map.models import *
from map.serializers import *
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from utilities.flight import api_response
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
import copy
from django.db.models import Q
import gc
import json
from xml.dom import minidom
import uuid
from utilities.redis_storage import *
from utilities.flight import flight_booking_save, ticket_issue, make_ticket_data
from utilities.utils import *
from travel_api.serializers import *
import utilities.config as config
from datetime import datetime
from credentials.credentials import Credentials
from admin_dashboard.modules.config_parameter import *


class AuthToken(ObtainJSONWebToken):
    @swagger_auto_schema(responses={200: AuthTokenSerializer(many=True)})
    def post(self, request, *args, **kwargs):
        # by default attempts username / passsword combination
        response = super(AuthToken, self).post(request, *args, **kwargs)
        # token = response.data['token']  # don't use this to prevent errors
        # below will return null, but not an error, if not found :)
        res = response.data
        token = res.get('token')
        req = request.data  # try and find email in request
        username = req.get('username')

        # token ok, get user
        if token:
            agent = User.objects.filter(username=username)
            agent_id = Agent.objects.filter(user__username=username).get().id
            role_no_permission = RoleGranted.objects.filter(user_id=agent_id, role_id=-1)
            if role_no_permission:
                return Response(api_response(success=False, code=status.HTTP_406_NOT_ACCEPTABLE,
                                             message='User not allowed to login, please contact with your provider',
                                             response="User Authentication", data=req))
            user = AuthTokenSerializer(instance=agent.get()).data

            permission = PermissionGranted.objects.filter(role__rolegranted__user=agent_id)
            permission = PermissionGrantedSerializer(permission, many=True).data
            role = []
            if len(permission) > 0:
                role = Role.objects.filter(id=permission[0]['role'])
                role = RoleSerializer(role, many=True).data

            return Response({'success': True,
                             'message': 'Successfully logged in',
                             'response': 'User Authentication',
                             'token': token,
                             'data': user,
                             'permission': permission,
                             'role': role},
                            status=status.HTTP_200_OK)
        else:
            return Response(api_response(success=False, code=status.HTTP_401_UNAUTHORIZED,
                                         message='Failed, Incorrect password / User',
                                         response="User Authentication", data=req))