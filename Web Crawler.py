import requests, xml.etree.ElementTree as et, shutil, os
from HtmlTagNames import html_tag_names

def main(): 
    if not os.path.exists("./Downloads"):
        os.mkdir("./Downloads")
    if not os.path.exists("./History/"):
        os.mkdir("./History/")

    link = input("Please insert a valid link to a website: ")
    link = verify_link(link)

    request = requests.get(link)
    html = request.text

    with open("History/"+link[link.find("/")+2:-1]+".txt", "w+", encoding="UTF-8") as file:
        file.write(html)

    html = close_tags(html) # XML valid string of website
    elmtree = et.ElementTree(et.fromstring(html)) # XML tree of website

    tag = decide_tag()
    if tag=="img":
        sources = [x.attrib["src"] for x in elmtree.iter(tag)]
    elif tag=="video" or tag=="audio":
        sources = [x.find("source").attrib["src"] for x in elmtree.iter(tag)]
    else:
        sources = [x.te for x in elmtree.iter(tag)]



def close_tags(tree: str):
    tags: list[list[str, int]] = []
    x = 0
    while x != len(tree):
        # handle escaped back slashes
        if tree[x+1:x+2] == "\\":
            tree = tree.replace(tree[x:x+2],tree[x])
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
def download(link: str | list[str], directory="./Downloads/"):
    if not os.path.exists(directory):
        os.mkdir(directory)
    
    if type(link) == "list":
        for x in link:
            image_name = x[len(x)-x[::-1].find("/"):]
            with open(directory+image_name, "wb") as img:
                shutil.copyfileobj(requests.request("GET", link+x, stream=True).raw, img)
    else:
        image_name = x[len(x)-x[::-1].find("/"):]
        with open(directory+image_name, "wb") as img:
            shutil.copyfileobj(requests.request("GET", link+x, stream=True).raw, img)
def verify_link(domain: str):
    if domain[:7] != "http://" and domain[:8] != "https://":
        domain = "http://"+domain
    if domain[-1] != "/":
        domain += "/" 
    return domain
def decide_tag():
    print("Please decide which tags to download: ")
    print("1. Images.")
    print("2. Videos.")
    print("3. Audios.")
    print("4. Others.")
    while True:
        tag = int(input())
        match tag:
            case 1:
                return "img"
            case 2:
                return "video"
            case 3:
                return "audio"
            case 4:
                while True:
                    tag = input("Please specify tag: ")
                    if tag in html_tag_names:
                        break
                    print("Chosen tag does not exist, please input a correct tag.")
                return tag
            case _:
                print("Error. Please choose a correct number.")


main()