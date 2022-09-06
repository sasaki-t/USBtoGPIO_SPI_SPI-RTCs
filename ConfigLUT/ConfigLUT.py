﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file ConfigLUT.py
 @brief one-dimensional lookup table (LUT) component
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
configlut_spec = ["implementation_id", "ConfigLUT", 
         "type_name",         "ConfigLUT", 
         "description",       "one-dimensional lookup table (LUT) component", 
         "version",           "1.0.0", 
         "vendor",            "TakeshiSasaki", 
         "category",          "generic", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         "conf.default.table", "0,1,2,3",

         "conf.__widget__.table", "text",

         "conf.__type__.table", "string",

         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class ConfigLUT
# @brief one-dimensional lookup table (LUT) component
# 
# 1次元のLookup Table
# (LUT)コンポーネント。コンフィギュレーションでLUTの値となる整数のリストを指定する
# 。要素番号を入力ポートから指定するとLUTの対応する値が出力ポートから出力される。
# 範囲外の要素の番号が指定された場合は何も行わない。
# 
# InPort
# ポート名/型/説明
# indext/TimedLong/値を出力するLUTの要素番号。先頭要素の番号は0番とする。負の値を
# 入力した場合は、-1であれば最終要素の値、-2であれば最終要素の1つ前の値というよう
# に、逆順に数えた要素の値を出力する。
# OutPort
# ポート名/型/説明
# value/TimedLong/LUTの指定された要素の値。
# 
# 
# </rtc-template>
class ConfigLUT(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_index = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        値を出力するLUTの要素番号。先頭要素の番号は0番とする。負の値を入力した場合は
        、-1であれば最終要素の値、-2であれば最終要素の1つ前の値というように、逆順に数
        えた要素の値を出力する。
            - Type: RTC::TimedLong
         - Number: 1
        """
        self._indexIn = OpenRTM_aist.InPort("index", self._d_index)
        self._d_value = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        LUTの指定された要素の値。
         - Type: RTC::TimedLong
         - Number: 1
        """
        self._valueOut = OpenRTM_aist.OutPort("value", self._d_value)


        


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
        """
        LUTの値。値はカンマ区切りで指定する（カンマ区切りで値を増減することで要素数を
        変更可能）。各要素は整数値で指定する。
         - Name: table table
         - DefaultValue: 0,1,2,3
        """
        self._table = ['0,1,2,3']
        
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
        self.bindParameter("table", self._table, "0,1,2,3")
        
        # Set InPort buffers
        self.addInPort("index",self._indexIn)
        
        # Set OutPort buffers
        self.addOutPort("value",self._valueOut)
        
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
    
    ###
    ##
    ## The activated action (Active state entry action)
    ##
    ## @param ec_id target ExecutionContext Id
    ## 
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onActivated(self, ec_id):
    #
    #    return RTC.RTC_OK
    
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
    # コンフィギュレーションから値を読み込み、LUTを作成する。入力ポートから要素番号
    # の値を読み込み、LUTから対応する値を出力する。
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onExecute(self, ec_id):
        if self._indexIn.isNew():
            self._d_index = self._indexIn.read()
            try:
                LUT = list(map(int, self._table[0].split(",")))
                self._d_value.data = LUT[self._d_index.data]
                print(f'output={self._d_value.data}')
                self._valueOut.write()
            except ValueError:
                print('Invalid configuration value (table): value not integer')
                return RTC.RTC_ERROR
            except IndexError:
                print('Invalid input value (index): out of range')

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
    



def ConfigLUTInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=configlut_spec)
    manager.registerFactory(profile,
                            ConfigLUT,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ConfigLUTInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("ConfigLUT" + args)

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

