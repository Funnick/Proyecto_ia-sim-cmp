class Lexer:
    def __init__(self, program: str) -> None:
        self._text = self._read_program(program)
        self._text_lenght = len(self._text)
        self._pointer = 0
        self._current_char = None
        self._line = 1
        self._column = 1
        self._column_before_newline = 1
        self._breakline = False

    def _read_program(self, program: str) -> str:
        with open(program, "r") as file:
            return file.read()

    def move_next(self) -> bool:
        if self._pointer == self._text_lenght:
            return False
        # if self._pointer < self._text_lenght - 1:
        else:
            self._column = self._column + 1

            self._current_char = self._text[self._pointer]
            self._pointer = self._pointer + 1

            if self._current_char == "\n":
                self._line = self._line + 1
                self._column_before_newline = self._column
                self._column = 1
            return True

    def move_back(self, index_back: int) -> bool:
        if self._pointer - index_back >= 0 and index_back > 0:
            i = index_back
            point = self._pointer
            # new_col = self._column
            while i > 0:
                point = point - 1
                self._column = self._column - 1
                if self._text[point] == "\n":
                    self._column = self._column_before_newline - 1
                    self._line = self._line - 1
                i = i - 1

            self._pointer = self._pointer - index_back
            self._current_char = self._text[self._pointer]
            #    self._column = self._column - index_back
            return True
        return False

    @property
    def current(self):
        return self._current_char

    @property
    def get_line_column(self):
        return self._line, self._column

    def is_end(self) -> bool:
        return self._pointer == self._text_lenght
