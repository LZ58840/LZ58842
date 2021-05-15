class RemoveComment:
    def __init__(self):
        self.violations = {}

    def add_violation(self, rule, comment):
        if rule in self.violations:
            self.violations[rule] += ", " + comment
        else:
            self.violations[rule] = comment

    def is_empty(self):
        return self.to_string() == ""

    def to_string(self):
        content = ""
        if len(self.violations) > 0:
            content = "removed, "
            for rule in self.violations.keys():
                content += "rule " + str(rule) + ": "
                content += self.violations[rule]
                content += ".\n\n; "
            content = content.rstrip("; ")
        return content


class NoteComment:
    def __init__(self):
        self.content = ""

    def add_note(self, note):
        if self.is_empty():
            self.content = note
        else:
            self.content += ", " + note

    def is_empty(self):
        return self.content == ""

    def to_string(self):
        return "note: " + self.content
