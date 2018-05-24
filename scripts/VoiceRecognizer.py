#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import rospy
import subprocess
from geometry_msgs.msg import Twist
from std_msgs.msg import String 
import time
import json

class VoiceRecognizer:
    def __init__(self):
        self.vocie_sub = rospy.Subscriber('voice_recog',String,self.Receive)

        self.follow_req_pub = rospy.Publisher('/chase/request',String,queue_size=10)
        self.changing_pose_req_pub = rospy.Publisher('/arm/changing_pose_req',String,queue_size=1)
        self.changing_pose_result_pub = rospy.Publisher('/arm_change/result',String,queue_size=1)
        self.vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)
                
        self.discovery_location_num = 0
        self.discovery_remember_num = 0
        self.command_num = 0
        self.sentence = ' '
        
        self.location_list = [
            [0,'kitchen','keep','key','cutting','year','bag','kill','kids','key gene','take us back to','kitty','キッチン'],
            [0,'living','leaving','levy','meeting','leading','being','evening','reading','active','media','リビング','オレフィン','livin','自民'],
            [0,'dining','died','death','ocean','ダイニング','ダイイング'],
            [0,'children','child','chear'],
            [0,'hallway','hall','host'],
            [0,'bartable','bar','table','bath','double','board'],
            [0,'balcony','bag on','about one','buck on','bargain','body going','balble'],
            [0,'bedroom','bit too','beat','bed to','but the room','bath room','but','back','better','ベッドルーム','bid to','メタル','ベッド','ルーム','ベルン','ネット'],
            [0,'entrance','interes','end of','his and the','around','enter','entire','end','anton','エントランス'],
            [0,'finish','フィニッシュ','フィッシュ']]
        self.remember_list = ['car','Car']
        self.command_list = [['follow','Follow Me','ハロウィン','Follow','Follow me','フォロー','フォロミー','ホロミン','ホミン'],
                             ['stop','Stop']]
    
    def JsonStringToDictation(self, _json):
        #print(_json)
        dictation = json.loads(_json) # jsonで書かれた文字列を辞書型にする
        # json.loadsでunicodeに変換された文字列をstrにする
        import types
        for key in dictation:
            key_type = dictation[key]
            if type(key_type) == unicode: # unicodeをstrにする
                #print(key_type)
                #print(dictation[key])
                dictation[key] = dictation[key].encode('utf-8')
        return dictation
            
    def Receive(self, _receive_str):
        dict_data = self.JsonStringToDictation(_receive_str.data)
        self.sentence = dict_data["word"]
        self.discovery_location_num = 0
        self.discovery_remember_num = 0
        self.command_num = 0 
        print 'receive voice is :',self.sentence
        if self.sentence != ' ':
            for num in range(0,len(self.location_list)):
                for words_num in range(1,len(self.location_list[num])):
                    if self.location_list[num][words_num] in self.sentence:
                        self.location_list[num][0] = self.sentence.count(self.location_list[num][words_num])                        
                    else:
                        print 'nothing'
                        pass
            if self.location_list[self.location_list.index(max(self.location_list))][0] > 0:
                print '送る文字は',self.location_list[self.location_list.index(max(self.location_list))][1]
                self.recog_location = self.location_list[self.location_list.index(max(self.location_list))][1]
                for num in range(0,len(self.location_list)): 
                    self.location_list[num][0] = 0
                self.location_list[self.location_list.index(max(self.location_list))][1] == 'Null'
                self.discovery_location_num = 1

            print 'finish location list'
            for num in range(0,len(self.remember_list)):
                #print 'word is:',self.remember_list[num]
                if self.remember_list[num] in self.sentence:
                    print '送る文字は',self.remember_list[num]
                    self.remember_place_pub.publish('car')
                    self.discovery_remember_num = 1
                else:
                    print 'nothing'
                    pass

            print 'finish remember list'

            print 'remember num is:',self.discovery_remember_num
            if self.command_num == 0 and self.discovery_location_num == 0 and self.discovery_remember_num == 0:
                print 'receive command'
                for num in range(0,len(self.command_list)):
                    for words_num in range(0,len(self.command_list[num])):
                        if self.command_list[num][words_num] in self.sentence:
                            self.command_num = 1
                            print 'command is: ',self.command_list[num][0]
                            if self.command_list[num][0] == 'follow':
                                self.follow_req_pub.publish('follow')
                                print 'follow start'
                            elif self.command_list[num][0] == 'stop':
                                self.follow_req_pub.publish('stop')
                        else:
                            print 'nothing'
                            pass

                        
if __name__ == '__main__':
    rospy.init_node('voice_recognizer',anonymous=True)
    voice_recognizer = VoiceRecognizer()
    rospy.spin()
    
