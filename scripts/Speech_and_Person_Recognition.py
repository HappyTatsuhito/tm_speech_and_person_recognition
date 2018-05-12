#!/usr/bin/env python
# -*- coding: utf-8 -*

import rospy
import time
from std_msgs.msg import String, Float64,Bool
import subprocess
from geometry_msgs.msg import Twist

class SpeechandPersonRecognition:
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)
        self.m6_pub = rospy.Publisher('/m6_controller/command',Float64,queue_size=1)
        self.navigation_req_pub = rospy.Publisher('/navigation/input',String,queue_size=1)
        self.crowd_list_req_pub = rospy.Publisher('/object/list_req',Bool,queue_size=1)

        self.crowd_list_res_sub = rospy.Subscriber('/object/list_res',String,self.getCrowdSizeCB)
        
        self.twist_cmd = Twist()
        self.m6_angle = Float64()
        self.crowd_list = []
        self.male_count = -1
        self.female_count = -1

    def getCrowdSizeCB(self,result):
        self.crowd_list = result.data.split(' ')
        self.crowd_list[-1:] = []
        self.male_count = crowd_list.count('male')
        self.female_count = crowd_list.count('female')
        

    def startSPR(self):#-----------------state 0
        print 'state : 0'
        self.m6_angle.data = -0.4
        self.m6_pub.publish(self.m6_angle)
        rospy.sleep(2.0)
        voice_cmd = '/usr/bin/picospeaker %s' %'I want to play riddle game!'
        subprocess.call(voice_cmd.strip().split(' '))
        rospy.sleep(3.0)
        rospy.sleep(10)
        self.twist_cmd.angular.z = 2.0
        for i in range(10):
            self.cmd_vel_pub.publish(self.twist_cmd)
            rospy.sleep(0.5)
            #180°回転させたい
        return 1

    def stateSizeOfTheCrowd(self):#------state 1
        print 'state : 1'
        #男女認識
        rospy.sleep(3.0)
        self.crowd_list_req_pub.publish(True)
        while self.male_count * self.female_count < 0 and not rospy.is_shutdown():
            print 'getting crowd size'
            rospy.sleep(1.0)
        voice_cmd = '/usr/bin/picospeaker %s' %'It is'
        subprocess.call(voice_cmd.strip().split(' '))
        voice_cmd = '/usr/bin/picospeaker %s' %str(self.male_count)
        subprocess.call(voice_cmd.strip().split(' '))
        voice_cmd = '/usr/bin/picospeaker %s' %'male and'
        subprocess.call(voice_cmd.strip().split(' '))
        voice_cmd = '/usr/bin/picospeaker %s' %str(self.female_count)
        subprocess.call(voice_cmd.strip().split(' '))
        voice_cmd = '/usr/bin/picospeaker %s' %'female.'
        subprocess.call(voice_cmd.strip().split(' '))
        rospy.sleep(3.0)
        voice_cmd = '/usr/bin/picospeaker %s' %'Who want to play riddles with me?'#オペレータを要求
        subprocess.call(voice_cmd.strip().split(' '))
        rospy.sleep(3.0)

        return 2

    def startRiddleGame(self):#----------state 2
        print 'state : 2'

        
        return 3

    def startBlindMansBluffGame(self):#--state 3
        print 'state : 3'


        return 4

    def leaveArena(self):#---------------state 4
        print 'state : 4'
        navigation_req = String()
        navigation_req.data = 'entrance'
        self.navigation_req_pub.publish

        return 5


if __name__ == '__main__':
    rospy.init_node('Speech_and_Person_Recognition')
    spr = SpeechandPersonRecognition()
    main_state = 0
    while main_state < 5 and not rospy.is_shutdown():
        if main_state == 0:
            main_state = spr.startSPR()
            #1,2
        elif main_state == 1:
            main_state = spr.stateSizeOfTheCrowd()
            #3
        elif main_state == 2:
            main_state = spr.startRiddleGame()
            #4
        elif main_state == 3:
            main_state = spr.startBlindMansBluffGame()
            #5
        elif main_state == 4:
            main_state = spr.leaveArena()
            #6
            
