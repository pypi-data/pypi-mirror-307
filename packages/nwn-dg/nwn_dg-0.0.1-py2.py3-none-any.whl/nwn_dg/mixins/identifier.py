class IdentifierMixin:
    def __init__(self, identifier=None):
        self._identifier = identifier
        self._current_identifier = self._identifier

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, rhs):
        self._identifier = rhs

    @property
    def current_identifier(self):
        if self._current_identifier is None:
            self._current_identifier = self._identifier
        return self._current_identifier

    @current_identifier.setter
    def current_identifier(self, rhs):
        self._current_identifier = rhs
