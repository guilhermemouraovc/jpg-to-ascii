from PIL import Image
def asciiConvert(imagem, tipo, salvarcomo, scale):
    scale = int(scale)

   
    img = Image.open(imagem)
    w,h = img.size

    # resize image (downscale)
    img.resize((w//scale, h//scale)).save("resized.%s" % tipo)

    # open new image
    img = Image.open("resized.%s" % tipo)
    w, h = img.size # get new width and height 


    # list with correct length and height (same as resized image)
    grid = []
    for i in range(h):
        grid.append(["X"] * w)

    pix = img.load()


    for y in range(h):
        for x in range(w):
            if sum(pix[x,y]) == 0:
                grid[y][x] = "#"
            elif sum(pix[x,y]) in range(1,100):
                grid[y][x] = "X"
            elif sum(pix[x,y]) in range(100,200):
                grid[y][x] = "%"
            elif sum(pix[x,y]) in range(200,300):
                grid[y][x] = "&"
            elif sum(pix[x,y]) in range(300,400):
                grid[y][x] = "*"
            elif sum(pix[x,y]) in range(400,500):
                grid[y][x] = "+"
            elif sum(pix[x,y]) in range(500,600):
                grid[y][x] = "/"
            elif sum(pix[x,y]) in range(600,700):
                grid[y][x] = "("
            elif sum(pix[x,y]) in range(700,750):
                grid[y][x] = "'"
            else:
                grid[y][x] = " "
                
    art = open(salvarcomo, "w")

    for row in grid:
        art.write("".join(row)+"\n")

    art.close()

if __name__ == '__main__':
    asciiConvert("C:\\Users\\gmvc\\Documents\\Meus scripst\\joto.jpg", "jpg", "julia", "3")
