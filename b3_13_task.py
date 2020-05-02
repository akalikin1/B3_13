class HTML:

    def __init__(self, output=None):
        self.output = output
        self.children = []
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        
        if self.output is None:
            print(self)

        else:
            print(f'Сохранение в файл {self.output}')
            with open(self.output, 'w') as file:
                file.write(str(self))

    def __str__(self):
        html = '<html>\n'
        for child in self.children:
            html += str(child)
        html += '</html>'
        return html

class TopLevelTag:
    def __init__(self, tag):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        TopLevel = f'<{self.tag}>\n'
        for child in self.children:
            TopLevel += str(child)
        TopLevel += f'\n</{self.tag}>\n'
        return TopLevel

class Tag:

    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None:  
            self.attributes[" class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(f'{attribute}="{value}"')
            
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            part1 = f'\n   <{self.tag}{attrs}>'
            
            if self.text:
                part2 = f'{self.text}'
            else:
                part2 = ""
            for child in self.children:
                part2 += '\n'+ str(child)
            part3 = f'   </{self.tag}>'
            return part1 + part2 + part3
        else:
            if self.is_single:
                return f'      <{self.tag}{attrs}/>\n'
            else:
                return f'      <{self.tag}{attrs}>{self.text}</{self.tag}>'   

with HTML(output='my.html') as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body