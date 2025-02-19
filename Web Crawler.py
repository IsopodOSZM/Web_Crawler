import requests, xml.etree.ElementTree as et

def main():
    # request = requests.request("GET", "https://books.toscrape.com")
    # html = request.text
    # with open("XMLs/toscrape.txt", "w+", encoding="UTF-8") as file:
    #     file.write(html)
    with open("XMLs/toscrape.txt", "r", encoding="UTF-8") as file:
        html = "".join(file.readlines())
    html = close_tags(html)
    elmtree = et.ElementTree(et.fromstring(html))
    print([x for x in elmtree.iter("p")])


def close_tags(tree: str):
    tags: list[list[str, int]] = []
    x = 0
    while x != len(tree):
        # handle escaped back slashes
        if test == "\\":
            test = tree[x:x+2]
            tree = tree.replace(tree[x:x+2],tree[x]) 
            test = tree[x:x+2]
        # handle comments and doctype
        if tree[x:x+2] == "<!":
            x = tree.find("-->", x)+2
        
        # remove latest element from array and handle non closed tags
        elif tree[x:x+2] == "</":
            closepos = tree.find(">",x)
            tag = tree[x+2:closepos]
            truetag = tags[-1][0]
            stopper = (tags[-1][0]).find(" ")
            if stopper != -1:
                truetag = truetag[:stopper]
            if truetag != tag:
                tree = tree.replace(tags[-1][0]+">", tags[-1][0]+" />", 1)
                del tags[-1]
                del tags[-1]
                x += 2
            elif truetag == tag:
                del tags[-1]
        # add element to array
        elif tree[x] == "<":
            closepos = tree.find(">",x)
            if tree[closepos-1:closepos+1] == "/>":
                openpos = tree.find("<", x+1)
                x = openpos
                continue
            tag = tree[x+1:closepos]
            tags.append([tag, closepos])
        # adjust pointer x position
        openpos = tree.find("<", x+1)
        if x == -1:
            break
        x = openpos
    return tree


main()