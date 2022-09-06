﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file CountChange.py
 @brief Count input data change
 @date $Date$

 @author 佐々木毅 (Takeshi SASAKI) <sasaki-t(_at_)ieee.org>

"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
countchange_spec = ["implementation_id", "CountChange", 
         "type_name",         "CountChange", 
         "description",       "Count input data change", 
         "version",           "1.0.0", 
         "vendor",            "TakeshiSasaki", 
         "category",          "generic", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.min", "0",
         "conf.default.max", "9",
         "conf.default.step", "1",
         "conf.default.change", "increase",

         "conf.__widget__.min", "text",
         "conf.__widget__.max", "text",
         "conf.__widget__.step", "text",
         "conf.__widget__.change", "radio",
         "conf.__constraints__.change", "(increase,decrease,change,nochange)",

         "conf.__type__.min", "int",
         "conf.__type__.max", "int",
         "conf.__type__.step", "int",
         "conf.__type__.change", "string",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class CountChange
# @brief Count input data change
# 
# 入力値が1つ前の入力値と比べ指定の変化をするたびに出力値が増加する。出力の変化範
# 囲、変化幅はコンフィギュレーションで変更可能。どのような変化をカウントするか（増
# 加する、減少する、変化する、変化しない）もコンフィギュレーションで指定できる。
# 例）min=0, max=4, step=2, change=increaseのとき、
# 入力値の変化が1→4→7→3→5→2→2→5なら入力値が増加した1→4で0、4→7で2、3→5で
# 4、0→5で0が出力される。
# 
# InPort
# ポート名/型/説明
# data/TimedLong/変化を検知する対象。
# OutPort
# ポート名/型/説明
# count/TimedLong/
# 入力値が変化するたびに出力される値。出力される値の範囲や変化のタイミングについて
# はコンフィギュレーションで指定できる。
# 
# 
# </rtc-template>
class CountChange(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_data = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        変化を検知する対象。
            - Type: RTC::TimedLong
         - Number: 1
        """
        self._dataIn = OpenRTM_aist.InPort("data", self._d_data)
        self._d_count = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        入力値が変化するたびに出力される値。出力される値の範囲や変化のタイミングにつ
        いてはコンフィギュレーションで指定できる。
         - Type: RTC::TimedLong
         - Number: 1
        """
        self._countOut = OpenRTM_aist.OutPort("count", self._d_count)


        


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        出力される値の最小値。min<=maxでなければならない。出力値が[min,
        max]の範囲を超えた場合、stepが正ならこの値が出力される。stepが非負のとき、最
        初に入力が指定の条件を満たしたときに出力される値もこの値になる。
         - Name: min min
         - DefaultValue: 0
        """
        self._min = [0]
        """
        出力される値の最大値。min<=maxでなければならない。出力値が[min,
        max]の範囲を超えた場合、stepが負ならこの値が出力される。stepが負のとき、最初
        に入力が指定の条件を満たしたときに出力される値もこの値になる。
         - Name: max max
         - DefaultValue: 9
        """
        self._max = [9]
        """
        指定された入力の変化を検知するたびに出力値が変化する幅。例えば、現在の出力値
        が0でstepが2なら次に出力される値は2、その次に出力される値は4となる。
         - Name: step step
         - DefaultValue: 1
        """
        self._step = [1]
        """
        出力ポートから値が出力されるタイミング。increaseの場合は入力値が1つ前の入力値
        と比べ増加した場合に、decreaseの場合は減少した場合に、changeの場合は増加もし
        くは減少した場合に、nochangeの場合は変化しなかった場合に出力ポートから値が出
        力される。
         - Name: change change
         - DefaultValue: increase
        """
        self._change = ['increase']
        
        # </rtc-template>


         
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
        self.bindParameter("min", self._min, "0")
        self.bindParameter("max", self._max, "9")
        self.bindParameter("step", self._step, "1")
        self.bindParameter("change", self._change, "increase")
        
        # Set InPort buffers
        self.addInPort("data",self._dataIn)
        
        # Set OutPort buffers
        self.addOutPort("count",self._countOut)
        
        # Set service provider to Ports
        
        # Set service consumers to Ports
        
        # Set CORBA Service Ports
        
        return RTC.RTC_OK
    
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
    
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ##
    # 初期化を行う。
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
        #clear buffer
        while self._dataIn.isNew():
            self._d_data = self._dataIn.read()

        self.received = False #flag if first input data is received or not
        self.sent = False #flag if first change is detected or not

        return RTC.RTC_OK
    
    ###
    ##
    ## The deactivated action (Active state exit action)
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onDeactivated(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ##
    # 入力ポートから値を読み込み、直前の入力値と比較する。入力値にコンフィギュレー
    # ションで指定の変化があれば出力を行う。
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):
        if self._min[0] > self._max[0]:
            print('Invalid configuration value: min > max')
            return RTC.RTC_ERROR

        while self._dataIn.isNew():
            self._d_data = self._dataIn.read()
            output_flag = False #unset flag

            if self.received: #if we have previous data
                #set flag if the input data changes as specified
                if self._change[0] == 'increase':
                    if self._d_data.data > self.data_prev:
                        output_flag = True
                elif self._change[0] == 'decrease':
                    if self._d_data.data < self.data_prev:
                        output_flag = True
                elif self._change[0] == 'change':
                    if self._d_data.data != self.data_prev:
                        output_flag = True
                elif self._change[0] == 'nochange':
                    if self._d_data.data == self.data_prev:
                        output_flag = True
            else: #first data
                self.received = True
            
            self.data_prev = self._d_data.data

            if output_flag: #change detected
                if self.sent:
                    #set output
                    self._d_count.data += self._step[0]
                    if self._d_count.data > self._max[0] or self._d_count.data < self._min[0]: #out of output range
                        self._d_count.data = self._min[0] if self._step[0]>=0 else self._max[0]
                else: #first detection
                    #set initial value
                    self._d_count.data = self._min[0] if self._step[0]>=0 else self._max[0]
                    self.sent = True

                print(f'output={self._d_count.data}')
                self._countOut.write()

        return RTC.RTC_OK
    
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
    
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
    



def CountChangeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=countchange_spec)
    manager.registerFactory(profile,
                            CountChange,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    CountChangeInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("CountChange" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

