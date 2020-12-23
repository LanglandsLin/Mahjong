# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 22:28:01 2020

@author: Langl
"""

import json
from random import choice
from MahjongGB import MahjongFanCalculator

class Mahjong():
    def __init__(self):
        self.input = json.loads(input())

        # 分析自己收到的输入和自己过往的输出，并恢复状态
        self.requests = self.input["requests"]
        self.responses = self.input["responses"]
        self.request = self.requests[-1].split()
        self.left_card = 21
        self.id = int(self.requests[0].split()[1])
        self.quan = int(self.requests[0].split()[2])
        self.turn = len(self.requests)
        self.recover()
        self.available_action()
        self.step()
        
    def recover(self):
        if self.turn < 2:
            self.hand = []
        else:
            self.hand = self.requests[1].split()[5:]
            self.desk = {}
            self.desk["PENG"] = []
            self.desk["GANG"] = []
            self.desk["CHI"] = []
            peng = ""
            gang = ""
            chi = ""
            for request, response in zip(self.requests[2:], self.responses[2:]):
                request = request.split()
                if int(request[0]) == 2:
                    self.left_card -= 1
                    self.hand.append(request[1])
                    
                if len(request) > 2 and request[2] == "PENG" and int(request[1]) == self.id:
                    self.hand.remove(request[-1])
                    self.hand.remove(peng)
                    self.hand.remove(peng)
                    self.desk["PENG"].append(peng)
                    
                if request[-1] == "GANG" and int(request[1]) == self.id:
                    self.hand = list(filter((gang).__ne__, self.hand))
                    self.desk["GANG"].append(gang)
                    
                if len(request) > 2 and request[2] == "BUGANG" and int(request[1]) == self.id:
                    self.hand.remove(request[-1])
                    self.desk["PENG"].remove(request[-1])
                    self.desk["GANG"].append(request[-1])
                    
                if len(request) > 2 and request[2] == "CHI" and int(request[1]) == self.id:
                    card1 = request[-2]
                    card1f = card1[0] + "{}".format(int(card1[1]) - 1)
                    card1p = card1[0] + "{}".format(int(card1[1]) + 1)
                    self.hand.append(chi)
                    if card1f in self.hand: self.hand.remove(card1f)
                    if card1 in self.hand: self.hand.remove(card1)
                    if card1p in self.hand: self.hand.remove(card1p)
                        
                    card2 = request[-1]
                    self.hand.remove(card2)

                    self.desk["CHI"].append(card1)
                
                response = response.split()
                if response[0] == "PLAY":
                    self.hand.remove(response[1])
                if response[0] == "PENG":
                    peng = request[-1]
                if response[0] == "GANG":
                    if len(response) == 1:
                        gang = request[-1]
                    else:
                        gang = response[-1]
                if response[0] == "CHI":
                    chi = request[-1]
                    
            
            self.hand.sort()
            
    def calculate_fan(self, card):
        desk_cards = []
        for key in self.desk:
            if len(self.desk[key]) != 0:
                for item in self.desk[key]:
                    desk_card = (key, item, 1)
                    desk_cards.append(desk_card)
        desk_cards = tuple(desk_cards)
        try:
            fan = MahjongFanCalculator(desk_cards, tuple(self.hand), card, 0, int(self.request[0]) == 2, False, False, self.left_card == 0, self.id, self.quan)
        except Exception as err:
            return 0
        else:
            fan_num = sum(list(zip(*fan))[0])
            return fan_num
        
    def check_gang(self, card):
        if self.left_card == 0:
            return False
        if self.hand.count(card) == 3:
            self.gang = card
            return True
        return False
    
    def check_angang(self, card):
        if self.left_card == 0:
            return False
        hand = self.hand + [card]
        hand_set = set(hand)
        hand_dict={}
        for item in hand_set:
            hand_dict.update({item:hand.count(item)})
            if hand_dict[item] == 4:
                self.angang = item
                return True
        return False
    
    def check_bugang(self, card):
        if self.left_card == 0:
            return False
        hand = self.hand + [card]
        for item in self.desk["PENG"]:
            if hand.count(item) == 1:
                self.bugang = item
                return True
        return False
    
    def check_hu(self, card):
        fan = self.calculate_fan(card)
        if fan < 8:
            return False
        else:
            return True
        
    def check_peng(self, card):
        if self.hand.count(card) == 2:
            self.peng = card
            return True
        return False
    
    def check_chi(self, card):
        if int(self.request[1]) == (self.id - 1) % 4:
            if self.check_shun(card, self.hand):
                return True
        return False
    
    def check_shun(self, card, hand):
        if card[0] == "F" or card[0] == "J":
            return False
        cardf = card[0] + "{}".format(int(card[1]) - 1)
        cardp = card[0] + "{}".format(int(card[1]) + 1)
        if cardf in hand and cardp in hand:
            self.chi = card
            return True
        cardf = card[0] + "{}".format(int(card[1]) - 1)
        cardff = card[0] + "{}".format(int(card[1]) - 2)
        if cardf in hand and cardff in hand:
            self.chi = cardf
            return True
        cardp = card[0] + "{}".format(int(card[1]) + 1)
        cardpp = card[0] + "{}".format(int(card[1]) + 2)
        if cardp in hand and cardpp in hand:
            self.chi = cardp
            return True
        return False
        
                
    def available_action(self):
        action_list = []
        if int(self.request[0]) == 2:
            self.left_card -= 1
            action_list.append("PLAY")
            card = self.request[1]
            if self.check_angang(card): action_list.append("ANGANG")
            if self.check_bugang(card): action_list.append("BUGANG")
            if self.check_hu(card): action_list.append("HU")
            self.card = card
        elif len(self.request) > 3 and int(self.request[0]) == 3 and int(self.request[1]) != self.id and self.request[2] != "BUGANG":
            card = self.request[-1]
            action_list.append("PASS")
            if self.check_peng(card): action_list.append("PENG")
            if self.check_chi(card): action_list.append("CHI")
            if self.check_gang(card): action_list.append("GANG")
            if self.check_hu(card): action_list.append("HU")
            self.card = card
        self.action_list = action_list
        
    def choose_card(self, hand):
        best_grade = 0
        best_card = choice(hand)
        for card in hand:
            hand_copy = hand.copy() 
            hand_copy.remove(card)
            grade = 3 * self.calculate_3n(hand_copy) + self.calculate_2(hand_copy) - self.calculate_hua(hand, card)
            if grade > best_grade:
                best_grade = grade
                best_card = card
        return best_card
    
    def calculate_3n(self, hand):
        n = 0
        hand_set = set(hand)
        for item in hand_set:
            if hand.count(item) >= 3:
                n += 1
        for item in hand:
            if self.check_shun(item, hand):
                n += 1
        return n
    
    def calculate_hua(self, hand, card):
        hua = []
        for item in hand:
            hua.append(item[0])
        hua_set = set(hua)
        hua_dict = {}
        for item in hua_set:
            hua_dict.update({item:hand.count(item)})
        return hua_dict[card[0]]
                
            
    def calculate_2(self, hand):
        m = 0
        hand_set = set(hand)
        for item in hand_set:
            if hand.count(item) == 2:
                m += 1
        return m
        
        
    def execute_action(self, action):
        if action == "HU":
            self.action = "HU"
        elif action == "ANGANG":
            self.action = "GANG {}".format(self.angang)
        elif action == "BUGANG":
            self.action = "BUGANG {}".format(self.bugang)
        elif action == "PLAY":
            hand = self.hand + [self.card]
            self.action = "PLAY {}".format(self.choose_card(hand))
        elif action == "GANG":
            self.action = "GANG"
        elif action == "PENG":
            hand = self.hand.copy()
            hand.remove(self.peng)
            hand.remove(self.peng)
            self.action = "PENG {}".format(self.choose_card(hand))
        elif action == "CHI":
            card = self.chi
            cardf = card[0] + "{}".format(int(card[1]) - 1)
            cardp = card[0] + "{}".format(int(card[1]) + 1)
            hand = self.hand + [self.card]
            if cardf in hand: hand.remove(cardf)
            if card in hand: hand.remove(card)
            if cardp in hand: hand.remove(cardp)
            self.action = "CHI {} {}".format(self.chi, self.choose_card(hand))
        else:
            self.action = "PASS"
            
            
            
    def step(self):
        if len(self.action_list) == 0:
            self.action = "PASS"
        else:
            if int(self.request[0]) == 2:
                action_list = ["HU", "ANGANG", "BUGANG", "PLAY"]
                for action in action_list:
                    if action in self.action_list:
                        self.execute_action(action)
                        break
            else:
                action_list = ["HU", "GANG", "PENG", "CHI", "PASS"]
                for action in action_list:
                    if action in self.action_list:
                        self.execute_action(action)   
                        break
        print(json.dumps({
            "response": self.action # 可以存储一些前述的信息，在该对局下回合中使用，可以是dict或者字符串
        }))
        
mahjong = Mahjong()
                