#!/usr/local/bin/python3.5

# Author : Stéphane Küng
#   Date : 6.1.2016

from Crypto.Hash import SHA256

class Subject:
    def __init__(self):
        self.specifications = {}

    def __repr__(self):
        return "-Subject Class-"

    def __str__(self):
        return str("Subject " + sha256(str(self.specifications))) 

class Node:
    def __init__(self, name, message):
        self.name = name
        self.childs = []
        self.criteria = []
        self.message = message

    def eval_subject(self, subject):

        print(self.message)

        if len(self.childs)>0:
            
            global_success = False 
            for child in self.childs:
                success = True
                for criterion in child.criteria:
                    try:
                        success = success and eval(str(subject.specifications[criterion.name]) + str(criterion.operator) + str(criterion.value))
                    except KeyError:
                        #print("criterion not in subject's specification : " + str(criterion.name))
                        success = False

                #print("        -> node : " + str(child.name) + " " + str("SUCCESS" if success else "FAILD"))
                global_success = global_success or success
                if success:
                    child.eval_subject(subject)
                    break

            #print("Global_success " + str(self.name) + " : " + str(global_success))
            if not global_success:
                print("Subject : {0}, node : {1}. You don't meet any child's criteria - This is a final node for you".format(subject, self.name))

        else:
            print("Subject : {0}, node : {1}. Your reach a final node".format(subject, self.name))

    def __repr__(self):
        return "-Node Class-"

    def __str__(self):
        return "Node : {0}, Childs : {1}, Criteria : {2} ".format(self.name, str([str(x) for x in self.childs]), str([str(x) for x in self.criteria]))

class Criterion:
    def __init__(self, name, operator, value):
        self.name = name
        self.valuetype = "float"
        self.value = value
        self.operator = operator

    def __repr__(self):
        return "-Criterion Class-"

    def __str__(self):
        return str("{0} {1} {2}".format(self.name, self.operator, self.value)) 
            
def sha256(data):
    return SHA256.new(data.encode()).hexdigest()[0:10]


n0 = Node("n0", "Root node")
n0.criteria.append(Criterion("temp","<",1000))
n1 = Node("n1", "Node 1")
n1.criteria.append(Criterion("temp",">",0))
n2 = Node("n2", "Node 2")
n2.criteria.append(Criterion("temp","<=",0))
n3 = Node("n3", "Node 3")
n3.criteria.append(Criterion("temp","<",-10))
n4 = Node("n4", "Node 4")
n4.criteria.append(Criterion("temp",">=",-10))
n5 = Node("n5", "Node 5")
n5.criteria.append(Criterion("temp","<",-20))
n6 = Node("n6", "Node 6")
n6.criteria.append(Criterion("temp",">",-5))
n7 = Node("n7", "Node 7")
n7.criteria.append(Criterion("temp",">",-30))
n7.criteria.append(Criterion("snow","<",3))
n8 = Node("n8", "Node 8")
n8.criteria.append(Criterion("snow",">=",3))
n8.criteria.append(Criterion("temp","<",-40))

n0.childs.append(n1)
n0.childs.append(n2)
n2.childs.append(n3)
n2.childs.append(n4)
n3.childs.append(n5)
n4.childs.append(n6)
n5.childs.append(n7)
n5.childs.append(n8)

s1 = Subject()
s1.specifications["temp"] = -45
s1.specifications["snow"] = 10

n0.eval_subject(s1)

