import re
from typing import List

class Box():
    """Represents a box inside the CLI"""

    def __init__(self, width: int, height: int, wrap: bool):
        """Initiaizes the Box with desired configuration
        :param width:   horizontal size of the box 
        :param height:  vertical size of the box
        :param wrap:    indicates if it should try to wrap long 
                        content in the box, otherwise it will be truncated
        """
        assert width > 0 and height > 0
        self._width = width
        self._height = height
        self._wrap = wrap
        self._content: List[str] = []

    
    def setContent(self, content:str):
        """Stablish the content of the box ensuring it fits inside the box (depending on it configuration)"""
        if self._wrap:
            self.__wrap_content_to_width(content)
        else:
            self.conent = content.split("\n")
            self.__truncate_content_width()

        self.__truncate_or_fill_content_height()

    def __wrap_content_to_width(self, content: str):
        """Wraps the content of given line in Box width"""
        for line in content.split("\n"):
            self._content = [line[i:i + self._width] for i in range(0, len(line), self._width)]

    def __truncate_content_width(self):
        """Truncates each content line in to Box's width"""
        self._content = [line[:self._width] for line in self._content]

    def __truncate_or_fill_content_height(self):
        """Truncates content size (height) to Box's height"""
        if len(self._content) > self._height:
            self._content = self._content[:self._height]
        elif len(self._content) < self._height:
            self._content += [" "*self._width] * (self._height - len(self._content))

    def getLines(self) -> List[str]:
        return self._content

    def join(self, box):
        assert type(self) == type(box)
        new_box = Box(self._width + box._width, max(self._height, box._height), self._wrap or box._wrap)
        content = ""
        for i in range(new_box._height):
            content += self._content[i]+"\n" if i < self._height else " "*new_box._width+"\n"
            content += box._content[i]+"\n" if i < box._height else " "*new_box._width+"\n"

        new_box.setContent(content)
        return new_box



class CommandLineBox():
    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height

    def _fill_box(self, string: str):
        self.height_margin = self.height - string.count("\n")
        marging = "\n"*int(self.height_margin/2) 
        return "%s%s%s" % (marging, string, marging)

    def render(self, string: str, vertically_filled=True):
        if vertically_filled:
            return self._fill_box(string)
        else:
            return string

    def render_cols(self, col_list_str: list, vertically_filled = True):
        n_cols = len(col_list_str)
        col_width = int(self.width/n_cols)
        col_max_height = max(l.count("\n") for l in col_list_str)

        frame_str = ""
        line_remaining = list()
        for line in range(col_max_height+1):
            line_str = ""
            for col in col_list_str:
                line_remaining.append(str())
                col_str = ""
                lines = col.split("\n")
                if len(lines) > line:
                    if len(lines[line]) - self._non_printable_len(lines[line]) > col_width - 1:
                        line_size = col_width-1 + \
                            self._non_printable_len(lines[line][0:col_width])
                        col_str += lines[line][0:line_size]
                        line_remaining[-1] = lines[line][line_size:len(
                            lines[line])]
                    else:
                        col_str += lines[line]
                col_fill_size = (col_width - len(col_str) +
                                 self._non_printable_len(col_str))
                line_str += col_str + " " * \
                    (col_fill_size if col_fill_size > 0 else 0)

            if any(line_remaining):
                for lr in line_remaining:
                    col_str = lr
                    col_fill_size = (col_width - len(col_str) +
                                     self._non_printable_len(col_str))
                    line_str += col_str + " " * \
                        (col_fill_size if col_fill_size > 0 else 0)
            line_remaining.clear()

            frame_str += line_str + "\n"
        if vertically_filled:
            return self._fill_box(frame_str)
        else:
            return frame_str

    def _non_printable_len(self, string: str):
        matches = re.findall("\x1b.[0-9]*m", string)
        return sum([len(m) for m in matches])
