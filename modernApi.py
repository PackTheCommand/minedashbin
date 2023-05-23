class API:

    """
    API-Methods here
    
    
    
    
    """


    class EventHandler:
        _events={"exampleEvent":[]}
        @classmethod
        def exapleEvent(func):
            API.EventHandler._events["exampleEvent"] +=[func]

    class triger:
        @classmethod
        def exapleEvent(event):
            for ef in API.EventHandler._events["exampleEvent"]:
                ef(event)

