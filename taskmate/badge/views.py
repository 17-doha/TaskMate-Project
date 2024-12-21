from django.shortcuts import render
from signup.models import User
from badge.models import UserBadge, Badge
from task.models import Task
from django.db.models import Q
import base64

# Create your views here.
