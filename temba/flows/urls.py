from django.conf.urls import url

from .views import FlowCRUDL, FlowLabelCRUDL, FlowRunCRUDL, FlowSessionCRUDL, PartialTemplate, MailroomCompletion

urlpatterns = FlowCRUDL().as_urlpatterns()
urlpatterns += FlowLabelCRUDL().as_urlpatterns()
urlpatterns += FlowRunCRUDL().as_urlpatterns()
urlpatterns += FlowSessionCRUDL().as_urlpatterns()
urlpatterns += [
    url(r"^partials/(?P<template>[a-z0-9\-_]+)$", PartialTemplate.as_view(), name="flows.partial_template"),
    url(r"^flow/mailroom/completion/?$", MailroomCompletion.as_view(), name="flows.mailroom_completion"),
]
