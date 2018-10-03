from assets.Element import * 
import random
import string

class TokenBuilder:
    def createRandomText(self, length):
        return "".join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + " " + " " + " " + " " + " " + " " + " " + " " + " " + " " + " " + " " + " " + " ") for _ in range(length))

    def createRandomMenuItemText(self):
        length_of_text = random.randint(7,12)
        return self.createRandomText(length_of_text)


    def createRandomHeadlineText(self):
        length_of_text = random.randint(10,15)
        return self.createRandomText(length_of_text)

    def createRandomParagraphText(self):
        length_of_text = random.randint(50,75)
        return self.createRandomText(length_of_text)

    def createRandomShortParagraphText(self):
        length_of_text = random.randint(25,35)
        return self.createRandomText(length_of_text)


    def createSidebar(self, num_of_buttons):
        sidebar = Element("sidebar", "")

        for _ in range(num_of_buttons):
            sidebar.addChildren(Element("sidebar-element", self.createRandomMenuItemText()))

        return sidebar

    def createMenu(self, logo_left, num_of_buttons):
        menu = Element("header", "")
        logo = None

        if logo_left:
            logo = Element("logo-left", "")
        else:
            logo = Element("logo-right", "")
        
        menu.addChildren(logo)

        for _ in range(num_of_buttons):
            menu.addChildren(Element("btn-inactive-white", self.createRandomMenuItemText()))

        return menu

    def createAllMenuPossibilities(self, max_num_buttons):
        
        menu_possibilities = []

        for i in range(2):
            for j in range(max_num_buttons+1):

                if i == 0:
                    logo_left = True
                else:
                    logo_left = False

                num_of_buttons = j
                menu = self.createMenu(logo_left, num_of_buttons)
                menu_possibilities.append(menu)

        return menu_possibilities

            
    def createRowElement(self, width):
        if not width in ["single", "double", "quadruple"]:
            print("wrong width given", width)
            raise

        grid_element = Element(width, "")

        headline = Element("small-title", self.createRandomHeadlineText())

        if width == "quadruple":
            text = Element("text", self.createRandomShortParagraphText())
        else:
            text = Element("text", self.createRandomParagraphText())

        button_type = random.choice(["btn-inactive-blue", "btn-inactive-black", "btn-inactive-grey"])
        button = Element(button_type, self.createRandomMenuItemText())

        grid_element.addChildren(headline)
        grid_element.addChildren(text)
        grid_element.addChildren(button)

        return grid_element

    # can create 5 different rows, check row_type 0 until 4
    def createRow(self, row_type):
        if not row_type in [0,1,2,3,4]:
            print("wrong row type given", row_type)
            raise
        
        types = {   0: ["single"],
                    1: ["double", "double"],
                    2: ["double", "quadruple", "quadruple"],
                    3: ["quadruple", "quadruple", "double"],
                    4: ["quadruple", "quadruple", "quadruple", "quadruple"]
                }

        row = Element("row", "")

        for element in types[row_type]:
            row.addChildren( self.createRowElement(element) )

        return row