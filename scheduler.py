import sched, time
from datetime import datetime as dt
import datetime
import vertigrow
from threading import Timer


#http://simeonfranklin.com/blog/2012/aug/14/scheduling-tasks-python/
def now_str():
    # Return hh:mm:ss string representation of the current time
    t = dt.now().time()
    return t.strftime("%H:%M:%S")

def print_it():
    print ('EXECUTED TIME:'+ now_str())

def dateToSeconds(date):
    # Returns the number of seconds until the date sent should occur
    if ((date-dt.now()).total_seconds() >= 0):
        print((date-dt.now()).total_seconds())
        return (date-dt.now()).total_seconds()
    else:
        return -1



class Scheduler(object):

    def __init__(self, name, vertiGrow):
        # Creates a Scheduler object whose name is *name*
        # and initializes a python "sched" object
        # Params:
        #   *name* sets the name of the object
        #   *vertiGrow* passes the vertiGrow object to be controlled
        self.sched_handle = sched.scheduler(time.time, time.sleep)

        self.vG = vertiGrow

        self.name = name
        self.eventDict = {}
        self.webEventList = []
        self.webEventDict = {}
        #daily_time = datetime.time(14, 55)
        #first_time = dt.combine(dt.now(), daily_time)
        #self.addEvent(time.mktime(first_time.timetuple()), 1, print_it, ())

    def addEventWeb(self, eventType, quantity, start_date, end_date, repeat, freq, eventTime, endTime, repeatDays):
        # Fill in documentation

        hour = int(eventTime[0:2])
        # Add 12 if in PM
        if (eventTime[6] == "P"):
            if (int(eventTime[0:2]) != 12):
                hour = int(eventTime[0:2]) + 12
            else:
                hour = 12

        # START DATE PARSE
        if (type(start_date) is not datetime.datetime):
            date_split = start_date.split('/')
            date = datetime.date(int(date_split.pop()), int(date_split.pop(0)), int(date_split.pop()))
            date_time = dt.combine(date, datetime.time(hour, int(eventTime[3:5])) )
            # Determine number of seconds until event occurs
            tte = dateToSeconds(date_time) # Time To Execution (TTE)
        else:
            tte = dateToSeconds(start_date)

        current_time = time.strftime("%Y-%m-%d %H:%M")
        end_hour = hour

        # Clean data to be sent to web server
        if (repeat != 'True'):
            repeat = False
            end_date_time = 0
        else:
            # END DATE PARSE for repeat
            if (type(end_date) is not datetime.datetime):
                end_date_split = end_date.split('/')
                end_date_dt = datetime.date(int(end_date_split.pop()), int(end_date_split.pop(0)), int(end_date_split.pop()))
                # END DATE CREATION
                end_date_time = dt.combine(end_date_dt, datetime.time(end_hour, int(eventTime[3:5])) )

        if (eventType == "water"):
            eventType = "Water"
        elif (eventType == "fertilize"):
            eventType = "Fertilize"
        elif (eventType == "lighting"):
            eventType = "LightingOn"
        elif (eventType == "lighting_off"):
            eventType = "LightingOff"

        if (type(endTime) == 'str'):
            # Run End Time operations
            end_hour = int(endTime[0:2])
            if (endTime[6] == "P"):
                if (int(endTime[0:2]) != 12):
                    end_hour = int(endTime[0:2]) + 12
                else:
                    end_hour = 12
        #if (type(end_date) is not datetime.datetime):
            # END DATE CREATION
        #    end_date_time = dt.combine(end_date_dt, datetime.time(end_hour, int(endTime[3:5])) )


        # eventID is the timestamp
        eventID = time.strftime("%Y%m%d%H%M%S")


        if (type(start_date) is not datetime.datetime):
            eventInfo = [eventID, eventType, quantity, date_time, end_date_time, repeat, freq, eventTime, endTime]
        else:
            eventInfo = [eventID, eventType, quantity, start_date, end_date, repeat, freq, eventTime, endTime]

        # String representation of event
        remEvent = "Event at " + str(current_time) + ": " + str(quantity) + " " + str(eventType) + " at " + str(eventTime) + "."

        # Case 0: no repeats
        if (repeat == False):
            if (eventType == "Water"):
                eventHandle = self.addEvent(eventID, tte, self.vG.water, (quantity,self.webEventList, eventInfo, self))
            elif (eventType == "Fertilize"):
                eventHandle = self.addEvent(eventID, tte, self.vG.fertilize, (self.webEventList, eventInfo))
            elif (eventType == "LightingOn"):
                eventHandle = self.addEvent(eventID, tte, self.vG.lighting, (self.webEventList, eventInfo, self))
            #elif (eventType == "LightingOff"):
            #    eventHandle = self.addEvent(eventID, tte, self.vG.lighting, (self.webEventList, eventInfo, self))
        # Case 1: repeats
        else:
            # Determine number of days until done repeating
            #t_delta = end_date_time - date_time
            #print(t_delta.days, " days for repeat.")
            # Check user-selected frequency
            if (freq != "custom"):
                if (eventType == "Water"):
                    eventHandle = self.addEvent(eventID, tte, self.vG.water, (quantity, self.webEventList, eventInfo, self))
                elif (eventType == "LightingOn" or eventType == "LightingOff"):
                    eventHandle = self.addEvent(eventID, tte, self.vG.lighting, (self.webEventList, eventInfo, self))
                elif (eventType == "Fertilize"):
                    print()
            elif (freq == "custom"):
                print("Custom!")


        # Only add to the web list if the event is after current time
        if (tte > 0):
            self.webEventList.append(eventInfo)
            # Match the unique eventID and the event info in the dict
            self.webEventDict[eventID] = eventInfo

        print("Items in the queue...")
        print(len(self.getQueue()))
        # If success
        return 1

    def getEventWeb(self, event):

        return 0

    def isEmpty(self):
        # Return: true if the event queue is empty
        return self.sched_handle.empty()

    def addEvent(self, eventID, tte, action, argument):
        # Adds an event to the scheduler
        # Return: the event that has been scheduled
        # Params:
        #   *eventID* is the unique id for the event to be added to dict
        #   *tte* is the number of seconds until the event occurs
        #   *action* is the function to call when finished
        #   *argument* must be a sequence holding params for action
        #       (can be blank i.e. ())
        #
        try:
            assert tte > 0
            event = Timer(tte, action, argument)
            self.eventDict[eventID] = event
            event.start()
            print("Event started...")
            return event
        except:
            print("Could not add event: Datetime already occured")


    def cancelEvent(self, eventID):
        # Cancels an event previously scheduled
        # Params:
        #   *eventID* is the unique ID of the event that should be cancelled
        #

        #Remove from web-focused list/dict
        self.webEventList.remove(self.webEventDict[eventID])
        print("removed from webEventList")
        del self.webEventDict[eventID]
        print("removed from webEventDict")

        #Remove actual event from occuring
        self.eventDict[eventID].cancel()
        print("cancelled the event from occuring")
        del self.eventDict[eventID]
        print("removed from eventDict")



    def getQueue(self):
        # Return: a list containing upcoming events in the order they will run
        # A list of lists containing event parameters
        return self.webEventList

    def run(self):
        # Runs all scheduled events
        print("Running scheduler...")
        self.sched_handle.run()

if __name__ == "__main__":

    # Testing space
    sch = Scheduler("tester", vertigrow.vertiGrow("v_test"))

    print("Testing Scheduler class...")
    # Test that isEmpty() works - - - - -
    print("Testing isEmpty()...")
    try:
        assert sch.isEmpty() == True
        print("     Success!")
    except:
        print("     Failure!")

    # Test adding an event - - - - - - - -
    print("Testing addEvent()...")
    try:
        daily_time = datetime.time(23, 59)
        first_time = dt.combine(dt.now(), daily_time)
        event = sch.addEvent(time.mktime(first_time.timetuple()), 1, print_it, ())
        print("     Adding event...")
        assert sch.isEmpty() != True
        print("     Success!")
    except:
        print("     Failure!")

    # Test removing an event - - - - - - -
    print("Testing cancelEvent()...")
    try:
        print("     Removing event...")
        sch.cancelEvent(event)
        assert sch.isEmpty() == True
        print("     Success!")
    except:
        print("     Failure!")
