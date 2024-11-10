class Token:
    def __init__(self, token, startpos=-1,action='', change_seq=0):
        self._token = token
        self._startpos = startpos
        self._action = action
        self._change_seq = change_seq

    @property
    def startpos(self):
        return self._startpos

    @property
    def token(self):
        return self._token

    @property
    def action(self):
        return self._action

    @property
    def change_seq(self):
        return self._change_seq
    
    @startpos.setter
    def startpos(self, value):
        self._startpos = value
    
    @token.setter
    def token(self, value):
        self._token = value
    
    @action.setter
    def action(self, value):
        self._action = value
    
    @change_seq.setter
    def change_seq(self, value):
        self._change_seq = value

    def to_dict(self):
        return {
            'token': self.token,
            'action': self.action,
            'startpos': self.startpos,
            'change_seq': self.change_seq,
        }
