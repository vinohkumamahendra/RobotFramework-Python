class TracTicket:

    def __init__(self):
        self.name = None
        self.priority = None
        self.plannedStart = None
        self.plannedEnd = None
        self.noTestCase = None
        self.release = None
        self.version = None
        self.owner = None
        self.time = None
        self.task = None

    def __init__(self, name,priority,plannedStart, plannedEnd,noTestCase,release,version,owner,time,task):
        self.name = name
        if(priority.lower() == 'critical' and priority.lower() == 'blocker'):
            self.priority = "blocker"
        elif(priority.lower() == 'normal' and priority.lower() == 'major'):
            self.priority = "major"
        elif(priority.lower() == 'minor'):
            self.priority = "minor"
        else:
            self.priority = "minor"
        self.plannedStart = str(plannedStart)
        self.plannedEnd = str(plannedEnd)
        self.noTestCase = noTestCase
        self.release = str(release)
        self.version = str(version)
        self.owner = owner
        self.time = str(time)
        self.task = task

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        self.name = value

    @property
    def priority(self):
        return self.priority

    @name.setter
    def priority(self, value):
        self.priority = value

    @property
    def plannedStart(self):
        return self.plannedStart

    @name.setter
    def plannedStart(self, value):
        self.plannedStart = value

    @property
    def plannedEnd(self):
        return self.plannedEnd

    @name.setter
    def plannedEnd(self, value):
        self.plannedEnd = value

    @property
    def  noTestCase(self):
        return self.noTestCase

    @name.setter
    def noTestCase(self, value):
        self.noTestCase = value

    @property
    def release(self):
        return self.release

    @name.setter
    def release(self, value):
        self.release = value

    @property
    def version(self):
        return self.version

    @name.setter
    def version(self, value):
        self.version = value

    @property
    def owner(self):
        return self.owner

    @name.setter
    def owner(self, value):
        self.owner = value

    @property
    def time(self):
        return self.time

    @name.setter
    def time(self, value):
        self.time = value

    @property
    def task(self):
        return self.task

    @name.setter
    def task(self, value):
        self.task = value

    def printDetails(self):
        print("Name ",self.name)
        print("Priority ", self.priority)
        print("Planned Start date ", self.plannedStart)
        print("Planned End date ", self.plannedEnd)
        print("NOT ", self.noTestCase)
        print("release ", self.release)
        print("version ", self.version)
        print("Owner ", self.owner)
        print("Time ", self.time)
        print("Task ", self.task)

