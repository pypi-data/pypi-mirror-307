from NLarge.utils.Token import Token

class WordsUtil: 
    # Track changes for each token
    class ChangeLog:
        def __init__(self, orig_token):
            self.orig_token = orig_token
            self.change_logs = [] # List to track token changes over time
            self.add(orig_token.token, 'original', orig_token.change_seq)
            self._is_changed = False # token change flag

        def add(self, token, action, change_seq):
            # add change to log
            if action != 'original' and not self._is_changed:
                self._is_changed = True
            # append new token object to change log
            self.change_logs.append(Token(token=token, action=action, change_seq=change_seq))

        def update(self, idx, token=None, action=None, change_seq=None):
            if not self._is_changed:
                self._is_changed = True

            if token:
                self.change_logs[idx].token = token
            if action:
                self.change_logs[idx].action = action
            if change_seq:
                self.change_logs[idx].change_seq = change_seq

        def size(self):
            # count of changes
            return len(self.change_logs) - 1

        def is_changed(self):
            return self._is_changed

        def get_latest_token(self):
            # get most recent token from change log
            return self.change_logs[-1]

        def update_last_token(self, startpos):
            # update start pos of last token in log
            self.change_logs[-1].startpos = startpos

        def to_changed_dict(self):
            return {
                'orig_token': self.orig_token.token,
                'orig_startpos': self.orig_token.startpos,
                'new_token': self.get_latest_token().token,
                'new_startpos': self.get_latest_token().startpos,
                'change_seq': self.get_latest_token().change_seq,
                'action': self.get_latest_token().action
            }

        def to_dict(self):
            return {
                'orig_token': self.orig_token.to_dict(),
                'change_logs': [t.to_dict() for t in self.change_logs]
            }

    def __init__(self, words='', tokens=None):
        self.words = words
        self.tokens = self.token2obj(tokens) if tokens else []
        # total changes in this instance
        self.changed_count = 0
  
    
    def token2obj(self, tokens):
        # convert a list of raw tokens into ChangeLog objects 
        objs = []
        startpos = 0
        for t in tokens:
            # create a token object with its start position in the document
            token_obj = Token(token=t, startpos=startpos + self.words[startpos:].find(t))
            # Wrap the Token in a ChangeLog for tracking changes
            change_log = self.ChangeLog(orig_token=token_obj)
            objs.append(change_log)

            # Update the start position to account for this token and space 
            startpos += len(token_obj.token) + 1

        return objs
    
    def add_token(self, idx, token, action, change_seq):
        token_obj = Token(token=token, startpos=-1, action=action, change_seq=change_seq)
        change_log = self.ChangeLog(orig_token=token_obj)
        self.tokens.insert(idx, change_log)
    
    def add_change_log(self, idx, new_token, action, change_seq):
        self.changed_count += 1
        # access changelog at idx and add new token
        self.tokens[idx].add(new_token, action=action, change_seq=change_seq)

    def update_change_log(self, token_idx, change_idx=None, token=None, action=None, change_seq=None):
        #update current entry in token's changelog
        change_idx = self.tokens[token_idx].size() if change_idx is None else change_idx
        # modify token's changelog at idx with new values
        self.tokens[token_idx].update(change_idx, token=token, action=action, change_seq=change_seq)

    def get_token(self, idx):
        return self.tokens[idx]

    def get_original_tokens(self):
        return [t.orig_token.token for t in self.tokens]

    def get_augmented_tokens(self):
        return [t.get_latest_token().token for t in self.tokens if len(t.get_latest_token().token) > 0]

    def size(self):
        return len(self.tokens)

    def changed_count(self):
        return self.changed_cnt

    def get_change_logs(self, startpos=0):
        # update and rerturn list of changes, soirt by change seq
        for i, t in enumerate(self.tokens):
            # update start pos for each token based on the latest val
            self.tokens[i].update_last_token(startpos)
            # update start pos for next token
            startpos += len(t.get_latest_token().token)
            if len(t.get_latest_token().token) > 0:
                startpos += 1

        change_logs = [t for t in self.tokens if t.is_changed()]
        change_logs.sort(key=lambda x: x.get_latest_token().change_seq)
        return [c.to_changed_dict() for c in change_logs]