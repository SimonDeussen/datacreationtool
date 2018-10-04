class Element:
    def __init__(self, tag_name, content):
        
        self.valid_tags = ["body", "big-title", "small-title", "text", "btn-inactive-blue", "btn-inactive-white", "btn-inactive-black", "btn-inactive-grey", "header", "logo-left", "logo-right", "row", "single", "double", "quadruple", "sidebar", "sidebar-element"]

        
        if tag_name in self.valid_tags:
            self.tag_name = tag_name    
        else:
            print("tag not in valid tags " + tag_name)
            raise Exception("tag not in valid tags " + tag_name)

        self.content = content
        self.children = []

    def addChildren(self, child):
        self.children.append(child)

    def print(self):
        print(self.tag_name, self.content)

        if len(self.children) > 0:
            for child in self.children:
                child.toString(1)

    def toString2(self): 
        return self.createTokenString()

    def createTokenString(self):
        if len(self.children) == 0:
            return self.tag_name
        else:
            children =  ""
            for child in self.children:
                children += child.createTokenString() + ", "

            children = children[:-2]    

            return "\n" + self.tag_name + " {\n" + children.strip() + "\n}"

    def toString(self, depth):
        padding = "    " * depth
        print(padding, self.tag_name, self.content)

        if len(self.children) > 0:
            new_depth = depth+1
            for child in self.children:
                child.toString(new_depth)

    def render(self, dsl_mapping):
        if len(self.children) == 0:

            try:
                html = dsl_mapping[self.tag_name]

                if "[]" in html:
                    html = html.replace("[]", str(self.content))

            except Exception as e:
                print(e)
                html = "" + str(self.content)
                print("could not find tag in dsl", self.tag_name)
            
            return html

        else:
            try:
                html = dsl_mapping[self.tag_name]

                if "[]" in html:
                    html.replace("[]", str(self.content))

                if "{}" in html:
                    child_html = ""

                    for child in self.children:
                        child_html += child.render(dsl_mapping)

                    html = html.replace("{}", child_html)

            except Exception as e:
                print(e)
                html = "" + self.content
                print("could not find tag in dsl", self.tag_name)
            
            return html


