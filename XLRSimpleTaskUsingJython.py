#!/usr/bin/env python

import sys, string, time, os, re
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.xlrelease.domain import Task
from com.xebialabs.deployit.plugin.api.reflect import Type
from java.text import SimpleDateFormat

def createSimpleTask(phaseId, taskTypeValue, title, propertyMap):
    """
    Function that creats a simple task
    """
    parentTask = taskApi.newTask(taskTypeValue)
    parentTask.title = title
    parentTask.description = title
    sdf = SimpleDateFormat("yyyy-MM-dd hh:mm:ss")

    for item in propertyMap:
        if item.lower().find("date") > -1:
            if propertyMap[item] is not None and len(propertyMap[item]) != 0:
                parentTask.pythonScript.setProperty(item,sdf.parse(propertyMap[item]))
        else:
            parentTask.pythonScript.setProperty(item,propertyMap[item])

    taskApi.addTask(phaseId, parentTask)


server = "xldserver"
deploymentPackage ="mypackage"
environment ="myenv"
serverCI = configurationApi.searchByTypeAndTitle("xldeploy.XLDeployServer",str(server))[0]
currentPhase = getCurrentPhase()

createSimpleTask(currentPhase.id,
                 "xldeploy.Deploy",
                 "Deployment of {0} to {1}".format(deploymentPackage, environment),
                 {'server':serverCI,'deploymentPackage':deploymentPackage,'deploymentEnvironment':environment}
                )
 