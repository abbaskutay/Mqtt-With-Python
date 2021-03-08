
import paho.mqtt.client as mqtt
import time
import logging
from tkinter import *
import json

logging.basicConfig(level=logging.INFO)

mqtt.Client.connected_flag = False  # create flag in class


class Subscriber:
    client = mqtt.Client("abbas")

    # Here i have written variables that i use it everywhere

    def __init__(self):
        self.topics = {}
        self.host = StringVar()
        self.topic = StringVar()
        self.qos = IntVar(0)
        self.port = IntVar()

        self.client.on_log = self.on_log
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        self.client.on_disconnect = self.on_disconnect
        self.listOf_msg_topics = []
        self.topic_ack = []

        self.quantityOfMessages = 0
        self.listOfMesgs = []
        self.tagOfMessage = 1
        self.number_of_allMessages = 0

        self.sec = 0
        self.period = 0


    def on_log(self, client, userdata, level, buf):
        # logging.info(buf)
        pass
    # this callback helps to conncect to broker

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True  # set flag
            logging.info("connected OK")
        else:
            logging.info("Bad connection Returned code=" + str(rc))
            client.loop_stop()

    # this callback helps to disconnect from the broker

    def on_disconnect(self, client, userdata, rc):
        logging.info("client disconnected ok")

    # this callback helps to subscribe to the topics

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logging.info("in on subscribe callback result " + str(mid))
        for t in self.topic_ack:
            if t[1] == mid:
                t[2] = 1  # set acknowledged flag
                logging.info("subscription acknowledged  " + str(t[0]))
                client.suback_flag = True

    # this callback helps to receive messages .
    def on_message(self, client, userdata, message):

        topic = message.topic
        msgr2 = str(message.payload.decode("utf-8"))
        msgr2 = json.loads(str(message.payload.decode("utf-8")))


        # here it calculates messages that received and it put them to the listbox
        # but i does not put it the last item , i could not figure it out.
        logging.info(msgr2)

        if self.quantityOfMessages == 0:
            self.time1 = time.time()

        if self.period <= 1:
            timestamp2 = time.time()
            self.period = "%.d" % (timestamp2 - self.time1)
            self.period = int(self.period)
            self.topics[str(topic), self.tagOfMessage] = self.quantityOfMessages
            self.quantityOfMessages += 1

        else:
            self.number_of_allMessages += self.quantityOfMessages
            self.messages_HaveBeen_received.insert(END, f" in this loop {self.tagOfMessage} , quantity: {self.quantityOfMessages}")
            self.quantityOfMessages = 0
            self.tagOfMessage += 1
            self.period = 0

    #  this mehtod does many things one them is connecting and subscribing to the topic(s) and then it trigger the
    # the on_messages callback and it receive messages.

    def doWork(self):
        print("Connecting to broker ", self.host.get())

        try:
            self.client.connect(self.host.get())  # connect to self.broker
        except:
            print("can't connect")
            sys.exit(1)

        self.client.loop_start()  # Start loop

        while not self.client.connected_flag:  # wait in loop
            print("In wait loop")
            time.sleep(1)

        print("Subscribing now")

        if "," in self.topic.get():
            self.topics_splitted = self.topic.get().split(",")
            for j in (self.topics_splitted):
                self.listOf_msg_topics.append((j, 0))
            print("subscribing  " + str(self.listOf_msg_topics))

            for t in self.listOf_msg_topics:
                try:
                    r = self.client.subscribe(t, qos=int(self.qos.get()))
                    if r[0] == 0:
                        print("Subscription OK !")
                        logging.info("subscribed to topic " + str(t[0]) + " return code" + str(r))
                        self.topic_ack.append([t[0], r[1], 0])  # keep track of subscription

                except Exception as e:
                    logging.info("error on subscribe" + str(e))
                    self.client.loop_stop()  # Stop loop
                    sys.exit(1)
                print("waiting for all subs")
        else:
            try:
                self.listOf_msg_topics.append((self.topic.get(), 0))
                for i in self.listOf_msg_topics:
                    r1 = self.client.subscribe(i, qos=self.qos.get())
                    if r1[0] == 0:
                        print("Subscription OK !")
                        logging.info("subscribed to topic " + str(i[0]) + " return code" + str(r1))
                        self.topic_ack.append([i[0], r1[1], 0])  # keep track of subscription
            except Exception as e:
                logging.info("error on subscribe" + str(e))
                self.client.loop_stop()  # Stop loop
                sys.exit(1)
            print("waiting for sub")

        logging.info("it is acknowledged and it is going to receive messages now")

        self.showLabel.config(bg="green")

    # this method put the all message in  the listbox
    def show(self):
        self.number_Of_Messages_rec.insert(END,self.number_of_allMessages)
        print(self.topics.items())


class Gui1(Frame, Subscriber):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Subscriber.__init__(self)

        self.create_window()

    def create_window(self):
        self.grid()

        self.host_label2 = Label(self, text='The host name           >>>> :', font=('', '14', "bold"))
        self.host_label2.grid(row=0, column=0, sticky=W)

        self.port_label2 = Label(self, text='The port number       >>>> :', font=('', '14', "bold"))
        self.port_label2.grid(row=1, column=0, sticky=W, pady=6)

        self.qos_label2 = Label(self, text='The Qos Level            >>>> :', font=('', '14', "bold"))
        self.qos_label2.grid(row=2, column=0, sticky=W, pady=5)

        self.topic_label2 = Label(self, text='Topic                       '
                                             '     >>>> :', font=('', '14', "bold"))
        self.topic_label2.grid(row=3, column=0, sticky=W, pady=5)

        self.host_entry2 = Entry(self, textvariable=self.host.set("127.0.0.1"))
        self.host_entry2.grid(row=0, column=1, sticky=W, columnspan=2)
        self.port_entry2 = Entry(self, textvariable=self.port.set(1883))
        self.port_entry2.grid(row=1, column=1, sticky=W, columnspan=2)
        self.qos_entry2 = Entry(self, textvariable=self.qos.set(1))
        self.qos_entry2.grid(row=2, column=1, sticky=W, columnspan=2)
        self.topic_entry2 = Entry(self, textvariable=self.topic)
        self.topic_entry2.grid(row=3, column=1, sticky=W, columnspan=2)

        self.label_msg_receieved = Label(self, text='Messages have been received :', font=('', '14', "bold"))
        self.label_msg_receieved.grid(row=5, column=4)
        self.messages_HaveBeen_received = Listbox(self, bg="white", width=49, height=9, fg="red")
        self.messages_HaveBeen_received.grid(row=6, column=4)
        self.subscribeButton = Button(self, text="Subscribe", command=self.doWork)
        self.subscribeButton.grid(row=7, column=0, sticky=W, padx=65)
        self.disconnectButton = Button(self, text="Disconnect")
        self.disconnectButton.grid(row=7, column=1, sticky=W, padx=65)
        self.label_Number_msg = Label(self, text='Total Number Of messages:   \n    ⬇️  ',
                                      font=('', '14', "bold"))
        self.label_Number_msg.grid(row=1, column=4)

        self.number_Of_Messages_rec = Listbox(self, bg="white", width=14, height=2, fg="red")
        self.number_Of_Messages_rec.grid(row=2, column=4)

        self.showLabel = Label(self, text='', font=('', '14', "bold"), bg="red", width=10)
        self.showLabel.grid(row=3, column=4)

        self.show_Button= Button(self, text="Show Button",command=self.show)
        self.show_Button.grid(row=8, column=0, sticky=W, padx=65)


def main():
    if __name__ == '__main__':
        root = Tk()
        root.title('MQQT SUBSCRIBER')
        root.geometry('910x450')
        app = Gui1(root)
        root.mainloop()


main()







