class Behavior:
    def __init__(self, ghost):
        self.ghost = ghost
    
    def start(self):
        pass
    
    def update(self, dt):
        pass
    
    def finish(self):
        pass

#needs to be better defined here
class Scattering(Behavior):
    def start(self):
        self.ghost.scatter()
    
    def update(self, dt):
        pass
    
    def finish(self):
        pass

#needs to be better defined here
class Chasing(Behavior):
    def start(self):
        self.ghost.chase()
    
    def update(self, dt):
        pass
    
    def finish(self):
        pass

#needs to be better defined here
class Freight(Behavior):
    def start(self):
        self.ghost.startFreight()
    
    def update(self, dt):
        pass
    
    def finish(self):
        pass

#smarter behaviors would go here