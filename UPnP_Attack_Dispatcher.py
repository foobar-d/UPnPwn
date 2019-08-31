#! /usr/bin/env python 37
from dirtySOAP import *
from SOAP_Handler import *

class UPnP_Attack_Dispatcher:
	def __init__(self, target_Device):
		self.target_Device = target_Device
		self.target_Device_Name = target_Device.device_InfoBundle.deviceType
		self.target_Device_Address = target_Device.address

	def overflow_Check_Int(self, this_Action, this_Service, this_Device):
		dontDropIt = SOAP_Handler(self.target_Device_Address)
		for argument in this_Action.arguments:
			if argument.datatype.upper().contains("UINT"):
				this_Input = 0
				while this_Input < 10000000:
					dontDropIt.prepare_SOAP(this_Device, this_Action, this_Service)
					this_Input += 1

	#def overflow_Check_String(self, this_Action, this_Service, this_Device):


	def hail_Mary_Simple_Test(self):
		dontDropIt = dirtySOAP_Handler(self.target_Device_Address)
		total = 0
		for service in self.target_Device.service_List:
			for action in service.actions:
				print "		Now testing ", action.name, " in service ", service.name.strip(), " ."
				action.http_Codes = dontDropIt.handle_Some_SOAP(self.target_Device, action, service, "Dirty")
				#if 200 in action.http_Codes:
				dontDropIt.save_SOAP_Message(self.target_Device, action, service)
				total += 1
		print "		Conducted ", total, " tests in total."
		interactable_Count = 0
		h401_count = 0
		h500_count = 0
		for service in self.target_Device.service_List:
			for action in service.actions:
				if 200 in action.http_Codes:
					print "		Action: ", action.name, " in Service: ", service.name, " INTERACTABLE"
					interactable_Count += 1
				elif 401 in action.http_Codes:
					h401_count += 1
				elif 500 in action.http_Codes:
					h500_count += 1
				else:
					pass
					#print "		Action: ", action.name, " in Service: ", service.name, " NOT INTERACTABLE ############"
		print "		Total of ", interactable_Count, " actions interactable from ", total
		print "		Got ", h401_count, " total HTTP 401 Errors and ", h500_count, " total HTTP 500 Errors."

	def send_Dirty_SOAP(self, this_Action, this_Service):
		these_Status_Codes = set()
		dirt = raw_input("		Enter some dirt to send as an action argument > ")
		count = int(raw_input("		Number of packets to send > "))
		while count > 0:
			some_Status_Codes = dirtySOAP.handle_Dirty_SOAP(self.target_Device, this_Action, this_Service, dirt)
			for status_Code in some_Status_Codes:
				these_Status_Codes.add(status_Code)
			count -= 1
		return these_Status_Codes