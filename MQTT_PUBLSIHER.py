
import paho.mqtt.client as mqtt
import time
import logging
from tkinter import *
import json
import random
import string
from tkinter import ttk

logging.basicConfig(level=logging.INFO)
mqtt.Client.connected_flag = False  # create flag in class




class Publisher:
    client = mqtt.Client("abbas1")

    def __init__(self):

        # Here i have written variables that i use it everywhere
        self.topics = {}
        self.list_ofMesg_Num = []
        self.listOf_msg_topics = []
        self.topic_ack = []
        self.count2 = 0
        self.count3 = 0
        self.sumAll_messages = 0

        self.host = StringVar()
        self.topic = StringVar()
        self.loops = IntVar()
        self.msq = StringVar()
        self.qos = IntVar(0)
        self.port = IntVar()
        self.bit = IntVar()
        self.all_message = IntVar()

        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe

    def on_log(self, client, userdata, level, buf):
        pass

    # this callback helps to conncect to broker

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.client.connected_flag = True  # set flag
            logging.info("connected OK")
        else:
            logging.info("Bad connection Returned code=" + str(rc))
            self.client.loop_stop()

    # this callback helps to disconnect from the broker

    def on_disconnect(self, client, userdata, rc):
        logging.info("client disconnected ok")

    def on_publish(self, client, userdata, mid):
        pass
        # logging.info("In on_pub callback mid= " + str(mid))

    # this callback helps to subscribe to the topics

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info("in on subscribe callback result " + str(mid))
        for t in self.topic_ack:
            if t[1] == mid:
                t[2] = 1  # set acknowledged flag
                logging.info("subscription acknowledged  " + t[0])
                client.suback_flag = True

    # this callback helps to know whether is subscribed or not

    def check_subs(self):
        # returns flase if have an unacknowledged subsription
        for k in self.topic_ack:
            if k[2] == 0:
                logging.info("subscription to " + k[0] + " not acknowledged")
                return (False)
        return True

    #  this method does the random staff and yields the random messages for us
    def randomString(self,stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))


    # this method trigger the connect callback and do some algortihm to connect it
    def connectToHost(self):
        print("Connecting to broker ", self.host.get())
        try:
            self.client.connect(self.host.get())  # connect to broker
        except:
            print("can't connect")
            print(self.host.get())
            sys.exit(1)
        self.client.loop_start()  # Start loop
        # self.client.loop_forever()

        while not self.client.connected_flag:  # wait in loop
            print("In wait loop")
            time.sleep(1)

    # this method helps to subscribe to the topic(s)
    def subscribeToTopic(self):

        if "," in self.topic.get():
            self.topics_splitted = self.topic.get().split(",")
            for j in (self.topics_splitted):

                self.listOf_msg_topics.append((j, 0))

        else:
            self.listOf_msg_topics.append((self.topic.get(), 0))


    # this method does the manual publishing which is not send random messages

    def pubslishManual(self):
        self.count = 0
        self.sec = 0
        self.num_sec = 1
        self.msq_normal=self.msq.get()


        #  here i just calculate the elapsed time and publsih it in every second
        loops = self.loops_entry.get()
        timestamp1 = time.time()

        while self.sec < int(loops):
            timestamp2 = time.time()
            period = "%.d" % (timestamp2 - timestamp1)
            period = int(period)

            for i in range(len(self.listOf_msg_topics)):
                print("Publishing topic= ", self.listOf_msg_topics[i][0], " message1= ", self.msq_normal + f"{self.sec}",
                      self.count)
                self.client.publish(self.listOf_msg_topics[i][0], str(json.dumps(self.msq_normal+f"{self.sec}")), qos=int(self.qos.get()))

            self.count += 1

            if period == self.sec:
                pass

            elif period != self.sec:
                self.list_ofMesg_Num.extend([(self.msq.get(),self.count)])
                self.count = 0
                self.sec += 1
                continue

            else:
                break

        for n,t in self.list_ofMesg_Num:
            self.messages_HaveBeen_Sent.insert(END, f"In loop {self.num_sec} , message {n}, quantiy :{t}")
            self.num_sec += 1
            self.sumAll_messages += t

        self.all_messages.insert(END, self.sumAll_messages)


    # this method does random publishing which takes random messages from random function

    def publishRandom(self):
        self.count = 0
        self.sec = 0
        self.num_sec = 1
        loops = self.loops_entry.get()

        self.rand_mesq = StringVar()
        self.random1 = self.randomString()
        self.rand_mesq.set(self.random1)

        #  here i just calculate the elapsed time and publsih it in every second

        timestamp1 = time.time()
        while self.sec < int(loops):
            timestamp2 = time.time()
            period = "%.d" % (timestamp2 - timestamp1)
            period = int(period)

            for i in range(len(self.listOf_msg_topics)):
                print("Publishing topic= ", self.listOf_msg_topics[i][0], " message1= ", self.rand_mesq.get(),
                      self.count)

                self.client.publish(self.listOf_msg_topics[i][0], str(json.dumps(self.rand_mesq.get()+f"{self.sec}")), qos=int(self.qos.get()))
            self.count += 1

            if period == self.sec:
                pass

            elif period != self.sec:
                self.list_ofMesg_Num.extend([(self.rand_mesq.get(), self.count)])
                self.random1 = json.dumps(self.randomString())

                self.rand_mesq.set(self.random1)
                self.count = 0
                self.sec += 1
                continue

            else:
                break

        # here i put it to the listbox
        for j, k in self.list_ofMesg_Num:
            self.messages_HaveBeen_Sent.insert(END, f"In loop {self.num_sec} , message {j}, quantiy :{k}")
            self.num_sec += 1
            self.sumAll_messages += k

        self.all_messages.insert(END, str(self.sumAll_messages))


    # this method triggers the main method in order of if condtions

    def do_work(self):
        self.connectToHost()
        self.subscribeToTopic()

        if self.bit.get() == 1:
            self.publishRandom()
        else:
            self.pubslishManual()

    #  this method does the disconnect staff
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()





# this whole class just creates the gui OOP staffs and use inherit from above class in order to use its methods to
# implement the functions.

class Gui1(Frame, Publisher ):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Publisher.__init__(self)
        self.initUI()
        self.master = parent

    def initUI(self):
        self.grid()
        self.host_label = Label(self, text='The host name           >>>> :', font=('', '14', "bold"))
        self.host_label.grid(row=0, column=0, sticky=W + N)
        self.port_label = Label(self, text='The port number       >>>> :', font=('', '14', "bold"))
        self.port_label.grid(row=1, column=0, sticky=W, pady=6)
        self.qos_label = Label(self, text='The Qos Level            >>>> :', font=('', '14', "bold"))
        self.qos_label.grid(row=2, column=0, sticky=W, pady=5)
        self.topic_label = Label(self, text='Topic                       '
                                            '     >>>> :', font=('', '14', "bold"))
        self.topic_label.grid(row=3, column=0, sticky=W, pady=5)

        self.loop_label = Label(self, text='Number of loops       >>>> :', font=('', '14', "bold"))
        self.loop_label.grid(row=4, column=0, sticky=W, pady=5)
        self.messages_label = Label(self, text='Messages will be sent : \n\n   ⬇️ ', font=('', '14', "bold"))
        self.messages_label.grid(row=5, column=0, sticky=W, pady=5)

        self.all_message_label = Label(self, text='Number of all messages have been sent:', font=('', '14', "bold"))
        self.all_message_label.grid(row=6, column=4, sticky=W)

        self.messages_toBe_Sent = Entry(self, bg="white", width=30, textvariable=self.msq)
        self.messages_toBe_Sent.grid(row=6, column=0, padx=2, pady=(0, 120))
        self.messages_toBe_Sent.config(highlightbackground="red")


        self.random_Button = Checkbutton(self, text="Random \n Meassages", font=("", "12", "bold"),variable=self.bit,onvalue=1,offvalue=0)
        self.random_Button.grid(row=5, column=1, padx=(0, 18))

        self.label_msg_sent = Label(self, text='Messages have been sent :', font=('', '14', "bold"))
        self.label_msg_sent.grid(row=4, column=4)
        self.messages_HaveBeen_Sent = Listbox(self, bg="white", width=40, height=9, fg="red")
        self.messages_HaveBeen_Sent.grid(row=5, column=4)

        self.host_entry = Entry(self, textvariable=self.host.set("127.0.0.1"))
        self.host_entry.grid(row=0, column=1, sticky=W, pady=2)
        self.port_entry = Entry(self, textvariable=self.port.set(1883))
        self.port_entry.grid(row=1, column=1, sticky=W, pady=2)
        self.qos_entry = Entry(self, textvariable=self.qos.set(1))
        self.qos_entry.grid(row=2, column=1, sticky=W, pady=2)
        self.topic_entry = Entry(self, textvariable=self.topic)
        self.topic_entry.grid(row=3, column=1, sticky=W, pady=2)
        self.loops_entry = Entry(self, textvariable=self.loops)
        self.loops_entry.grid(row=4, column=1, sticky=W, pady=2)

        self.all_messages = Entry(self, textvariable=self.all_message.set(None),width=10)
        self.all_messages.grid(row=7, column=4)

        self.disconnectButton = Button(self, text="Disconnect", command=self.disconnect)
        self.disconnectButton.grid(row=6, column=1, sticky=W, padx=65)
        self.publishButton1 = Button(self, text="Publish", command=self.do_work)
        self.publishButton1.grid(row=6, column=0, sticky=W, padx=65)


def main():
    if __name__ == '__main__':
        root = Tk()
        root.title('MQQT PUBLISHER')
        root.geometry('882x500')
        app = Gui1(root)
        root.mainloop()


main()
