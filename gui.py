import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import mysql.connector

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Passport Number:"))
        self.passport = TextInput(multiline=False)
        self.add_widget(self.passport)
        
        self.add_widget(Label(text="Visa Number:"))
        self.visa = TextInput(multiline=False)
        self.add_widget(self.visa)
        
        self.add_widget(Label(text="Age:"))
        self.age = TextInput(multiline=False)
        self.add_widget(self.age)
        
        self.add_widget(Label(text="Arrival Time:"))
        self.arrival = TextInput(multiline=False)
        self.add_widget(self.arrival)
        
        self.add_widget(Label(text="Departure Time:"))
        self.departure = TextInput(multiline=False)
        self.add_widget(self.departure)
        
        self.add_widget(Label(text="Terminal Number:"))
        self.terminal = TextInput(multiline=False)
        self.add_widget(self.terminal)
        
        self.add_widget(Label(text="Flight Number:"))
        self.flight = TextInput(multiline=False)
        self.add_widget(self.flight)
        
        self.add_widget(Label(text="Passenger UID:"))
        self.passenger = TextInput(multiline=False)
        self.add_widget(self.passenger)
        
        self.save_button = Button(text="\9Save", font_size=40)
        self.save_button.bind(on_press=self.save_passenger_info)
        self.add_widget(self.save_button)

    def save_passenger_info(self,instance):

        print("Passport Number: " + self.passport.text)
        print("Visa Number: " + self.visa.text)
        print("Age: " + self.age.text)
        print("Arrival Time: " + self.arrival.text)
        print("Departure Time: " + self.departure.text)
        print("Terminal Number: " + self.terminal.text)
        print("Flight Number: " + self.flight.text)
        print("Passenger UID: " + self.passenger.text)
        mydb = mysql.connector.connect(host='localhost', user='root', password='root007', database='EasyYatra')
        cur = mydb.cursor()
        query = "INSERT INTO passengerinfo (PassportNumber, VisaNumber, Age, ArrivalTime, DepartureTime, TerminalNumber, FlightNumber, PassengerUID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (self.passport.text, self.visa.text, self.age.text, self.arrival.text, self.departure.text, self.terminal.text, self.flight.text, self.passenger.text)
        cur.execute(query, values)
        mydb.commit()

        # reset the text of TextInput widgets after storing the data into the database
        self.passport.text = ""
        self.visa.text = ""
        self.age.text = ""
        self.arrival.text = ""
        self.departure.text = ""
        self.terminal.text = ""
        self.flight.text = ""
        self.passenger.text = ""    

        mydb.close()


class EasyYatra(App):
    def build(self):
        return MyGrid()

       
if __name__ == "__main__":
    EasyYatra().run()
