# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 22:28:01 2020

@author: Langl
"""

import json
from random import choice

class Mahjong():
    def __init__(self):
        self.input = json.loads(input())

        # 分析自己收到的输入和自己过往的输出，并恢复状态
        self.requests = self.input["requests"]
        self.responses = self.input["responses"]
        self.id = int(self.requests[0].split()[1])
        self.quan = int(self.requests[0].split()[2])
        self.turn = len(self.requests)
        self.recover()
        
    def recover(self):
        if self.turn < 2:
            self.hand = []
        else:
            self.hand = self.requests[1].split()[5:]
            self.desk = []
            self.responses.append("PASS")
            for request, response in zip(self.requests[2:], self.responses[2:]):
                request = request.split()
                if int(request[0]) == 2:
                    self.hand.append(request[1])
                    
                if len(request) > 2 and request[2] == "PENG" and int(request[1]) == self.id:
                    self.hand.remove(request[-1])
                    self.hand.remove(self.peng)
                    self.hand.remove(self.peng)
                    self.desk.append(self.peng+"*3")
                    
                if request[-1] == "GANG" and int(request[1]) == self.id:
                    self.hand.remove(request[-1])
                    self.hand = list(filter((self.gang).__ne__, self.hand))
                    self.desk.append(self.gang+"*4")
                    
                if len(request) > 2 and request[2] == "BUGANG" and int(request[1]) == self.id:
                    self.hand.remove(request[-1])
                    self.desk.remove(request[-1]+"*3")
                    self.desk.append(request[-1]+"*4")
                    
                if len(request) > 2 and request[2] == "CHI" and int(request[1]) == self.id:
                    card1 = request[-2]
                    card1f = card1[0] + "{}".format(int(card1[1]) - 1)
                    card1p = card1[0] + "{}".format(int(card1[1]) + 1)
                    self.hand.append(self.chi)
                    if card1f in self.hand: self.hand.remove(card1f)
                    if card1 in self.hand: self.hand.remove(card1)
                    if card1p in self.hand: self.hand.remove(card1p)
                        
                    card2 = request[-1]
                    self.hand.remove(card2)

                    self.desk.append(card1f + card1 + card1p)
                
                response = response.split()
                if response[0] == "PLAY":
                    self.hand.remove(response[1])
                if response[0] == "PENG":
                    self.peng = request[-1]
                if response[0] == "GANG":
                    if len(response) == 1:
                        self.gang = request[-1]
                    else:
                        self.gang = response[-1]
                if response[0] == "CHI":
                    self.chi = request[-1]
                    
            
            self.hand.sort()
            
    def step(self):
        if int(self.requests[-1].split()[0]) == 2:
            self.action = "PLAY {}".format(choice(self.hand))
        else:
            self.action = "PASS"
            
        print(json.dumps({
            "response": self.action # 可以存储一些前述的信息，在该对局下回合中使用，可以是dict或者字符串
        }))
        
mahjong = Mahjong()
mahjong.step()
                
                